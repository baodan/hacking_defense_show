from flask import request, abort
from app.database import db
from tools.model_helper import obj_list_to_list_dict, obj_to_dict
from sqlalchemy import and_, or_
from flask import current_app
from math import ceil
from copy import deepcopy


def com_gets(model_cls, query_obj=None, args=None):
    # 获取get内容
    if args is None:
        # 自定义args
        args = request.args.to_dict()
        current_app.logger.debug('com_gets args: {}'.format(args))
    filters = []
    filter_by = {}
    if args:
        for name in args:
            # 字段模糊查询
            if args[name].startswith('like('):
                filters.append(getattr(getattr(model_cls, name), 'like')(args[name][5:-1]))
            # 字段内容包含查询
            elif args[name].startswith('in_('):
                filters.append(getattr(getattr(model_cls, name), 'in_')(args[name][4:-1].split(',')))
            # 字段内容不包含查询
            elif args[name].startswith('not_in_('):
                filters.append(~getattr(getattr(model_cls, name), 'in_')(args[name][8:-1].split(',')))
            # 正常字段值查询
            else:
                if name not in ['PAGE', 'PER_PAGE']:
                    filter_by[name] = args[name]
    # 自定义查询
    if query_obj:
        try:
            objs = query_obj.filter_by(**filter_by)
        except Exception as e:
            current_app.logger.error("{} customer filter_by exception: {}".format(model_cls, e))
            current_app.logger.error("customer filter_by: {}".format(filter_by))
            raise e
    # 正常键值对查询
    else:
        try:
            objs = model_cls.query.filter_by(**filter_by)
        except Exception as e:
            current_app.logger.error("{} key=value filter_by exception: {}".format(model_cls, e))
            current_app.logger.error("key=value filter_by: {}".format(filter_by))
            raise e
    # 有filter 内容时查询
    if filters:
        try:
            objs = objs.filter(and_(*filters))
        except Exception as e:
            current_app.logger.error("{} filters exception: {}".format(model_cls, e))
            current_app.logger.error("filters: {}".format(filter_by))
            raise e
    return objs


def com_post(db, model_cls, args=None):
    # 获取post内容
    if request.headers['Content-Type'] == 'application/json':
        if args is None:
            args = request.json
        current_app.logger.debug('com_post args: {}'.format(args))
    else:
        raise 'only support json data'
    if args:
        # 获取单个创建数据
        model_data = args
        # 数据需要为字典形式并存在
        if model_data and isinstance(model_data, dict):
            try:
                # 获取post内容
                obj = model_cls(**model_data)
            except Exception as e:
                current_app.logger.error("{} model init exception: {}".format(model_cls, e))
                current_app.logger.error("model_data: {}".format(model_data))
                raise e
            # 添加对象
            db.session.add(obj)
            try:
                # 同步数据到数据库
                db.session.commit()
            except Exception as e:
                current_app.logger.error("{} model init exception: {}".format(model_cls, e))
                current_app.logger.error("model_data: {}".format(model_data))
                raise e
            return obj

#批量创建
def com_posts(db, model_cls, args=None):
    # 获取post内容
    if request.headers['Content-Type'] == 'application/json':
        if args is None:
            args = request.json
        current_app.logger.debug('com_post args: {}'.format(args))
    else:
        raise 'only support json data'
    if args:
        # 获取多个创建数据
        model_datas = args
        # 数据需要为列表形式并存在
        if model_datas and isinstance(model_datas, list):
            data_list = []
            for model_data in model_datas:
                if model_data and isinstance(model_data,dict):
                    try:
                        # 获取post中多个创建内容
                        obj = model_cls(**model_data)
                        data_list.append(obj)
                    except Exception as e:
                        current_app.logger.error("{} model init exception: {}".format(model_cls, e))
                        current_app.logger.error("model_data: {}".format(model_data))
                        raise e
                    # 添加对象
            db.session.add_all(data_list)
            try:
                # 同步数据到数据库
                db.session.commit()
            except Exception as e:
                current_app.logger.error("{} model init exception: {}".format(model_cls, e))
                current_app.logger.error("model_datas: {}".format(model_datas))
                raise e
            return data_list
        

def com_get(model_cls, **filter_by):
    current_app.logger.debug('com_get filter_by: {}'.format(filter_by))
    try:
        # 查询数据
        obj = model_cls.query.filter_by(**filter_by).one()
    except Exception as e:
        current_app.logger.error("{} key=value filter_by exception: {}".format(model_cls, e))
        current_app.logger.error("key=value filter_by: {}".format(filter_by))
        raise e
    return obj


def com_put(db, model_cls, args=None, **filter_by):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        if args is None:
            args = request.json
        current_app.logger.debug('com_put filter_by: {}'.format(filter_by))
        current_app.logger.debug('com_put args: {}'.format(args))
    else:
        raise 'only support json data'
    if args:
        put_data = args
        if put_data:
            try:
                # 更新数据
                model_cls.query.filter_by(**filter_by).update(put_data)
            except Exception as e:
                current_app.logger.error("{} key=value filter_by exception update: {}".format(model_cls, e))
                current_app.logger.error('''filter_by: {}.
                put_data: {}.
                '''.format(filter_by, put_data))
                raise e
        try:
            # 同步数据到数据库
            db.session.commit()
        except Exception as e:
            current_app.logger.error("{} update db commit exception: {}".format(model_cls, e))
            raise e
        try:
            # 查询数据
            obj = model_cls.query.filter_by(**filter_by).one()
        except Exception as e:
            current_app.logger.error("{} key=value filter_by exception: {}".format(model_cls, e))
            current_app.logger.error("key=value filter_by: {}".format(filter_by))
            raise e
        return obj

#批量处理修改请求
def com_puts(db, model_cls,args=None):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        if args is None:
            args = request.json
        current_app.logger.debug('com_puts args: {}'.format(args))
    else:
        raise 'only support json data'
    if args:
        data_list = []
        put_datas = args
        if put_datas:
            for put_data in put_datas:
                id = put_data['id']
                msg = put_data.pop('id')
                try:
                    # 更新数据
                    model_cls.query.filter_by(id = id).update(msg)
                except Exception as e:
                    current_app.logger.error("{} key=value filter_by exception update: {}".format(model_cls, e))
                    current_app.logger.error('''filter_by: {}.
                    put_data: {}.
                    '''.format(id, put_data))
                    raise e
                try:
                    # 查询数据
                    obj = model_cls.query.filter_by(id = id).one()
                except Exception as e:
                    current_app.logger.error("{} key=value filter_by exception: {}".format(model_cls, e))
                    current_app.logger.error("key=value filter_by: {}".format(id))
                    raise e
                else:
                    data_list.append(obj)
            try:
                # 同步数据到数据库
                db.session.commit()
            except Exception as e:
                current_app.logger.error("{} update db commit exception: {}".format(model_cls, e))
                raise e
        return data_list


def com_del(db, model_cls, **filter_by):
    current_app.logger.debug('com_del filter_by: {}'.format(filter_by))
    try:
        # 查询数据
        model_cls.query.filter_by(**filter_by).delete()
    except Exception as e:
        current_app.logger.error("{} key=value filter_by delete exception: {}".format(model_cls, e))
        current_app.logger.error("key=value filter_by: {}".format(filter_by))
        raise e
    try:
        # 同步数据到数据库
        db.session.commit()
    except Exception as e:
        current_app.logger.error("{} delete db commit exception: {}".format(model_cls, e))
        raise e
    
    
def paginate(query, model_cls, page=None, per_page=None, error_out=False, max_per_page=None):
    """Returns ``per_page`` items from page ``page``.

    If ``page`` or ``per_page`` are ``None``, they will be retrieved from
    the request query. If ``max_per_page`` is specified, ``per_page`` will
    be limited to that value. If there is no request or they aren't in the
    query, they default to 1 and 20 respectively.

    When ``error_out`` is ``True`` (default), the following rules will
    cause a 404 response:

    * No items are found and ``page`` is not 1.
    * ``page`` is less than 1, or ``per_page`` is negative.
    * ``page`` or ``per_page`` are not ints.

    When ``error_out`` is ``False``, ``page`` and ``per_page`` default to
    1 and 20 respectively.

    Returns a : dict
    """

    if request:
        if page is None:
            try:
                page = int(request.args.get('PAGE', 1))
            except (TypeError, ValueError):
                if error_out:
                    abort(404)

                page = 1

        if per_page is None:
            try:
                per_page = int(request.args.get('PER_PAGE', 20))
            except (TypeError, ValueError):
                if error_out:
                    abort(404)

                per_page = 20
    else:
        if page is None:
            page = 1

        if per_page is None:
            per_page = 20

    if max_per_page is not None:
        per_page = min(per_page, max_per_page)

    if page < 1:
        if error_out:
            abort(404)
        else:
            page = 1

    if per_page < 0:
        if error_out:
            abort(404)
        else:
            per_page = 20

    items = query.limit(per_page).offset((page - 1) * per_page)

    if not items and page != 1 and error_out:
        abort(404)
        
    current_total = items.count()
    # No need to count if we're on the first page and there are fewer
    # items than we expected.
    if page == 1 and current_total < per_page:
        total = current_total
    else:
        total = model_cls.query.order_by(None).count()
    
    # The total number of pages
    if per_page == 0:
        pages = 0
    else:
        pages = int(ceil(total / float(per_page)))
        
    page_dict = {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "current_total": current_total
    }
    return page_dict
