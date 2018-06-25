from flask import make_response, current_app, request
from flask_security import auth_token_required
from flask_security import SQLAlchemyUserDatastore,\
    roles_accepted, roles_required
from app.models.user import User, Role, Group
from app.database import db
from app.urls import auth
from app.customer_error_class import InvalidMessage
from app.return_format import return_data
from flask_security.utils import verify_password
from tools.common_restful import com_put, com_post, com_del,\
    com_get, com_gets
from app.views.user_views import user_helper
from flask_security.utils import hash_password


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# @auth.route('/')
# def index():
#     return 'hello'


@auth.route('/get_token', methods=['POST'])
def get_token():
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    username = args.get('username', '')
    password = args.get('password', '')
    if username:
        # 获取用户对象
        try:
            user = user_datastore.find_user(username=username)
        except Exception as e:
            current_app.logger.error("[user][get] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
        if user:
            # 验证密码
            isok = verify_password(password, user.password)
            if not isok:
                raise InvalidMessage("password is invalid")
        else:
            raise InvalidMessage("username is not found")
    # 获取token
    try:
        token = user.get_auth_token()
    except Exception as e:
        current_app.logger.error("[user][get_auth_token] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    return return_data({'token': token}, 200)
    

@auth.route('/create_user', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_user():
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    user_dict = args.get('user', '')
    role_list = args.get('roles', '')
    group_list = args.get('groups', '')
    user_dict['password'] = hash_password(user_dict['password'])
    try:
        # 创建用户
        user = user_datastore.create_user(**user_dict)
    except Exception as e:
        current_app.logger.error("[user][post] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    if role_list:
        for role_id in role_list:
            #  获取角色对象
            try:
                role = com_get(Role, id=role_id)
            except Exception as e:
                current_app.logger.error("[role][get] fail expection: {}".format(e))
                raise InvalidMessage(str(e), 500)
            # 添加角色给用户
            try:
                user_datastore.add_role_to_user(user, role)
            except Exception as e:
                current_app.logger.error("[user][add_role] fail expection: {}".format(e))
                raise InvalidMessage(str(e), 500)
    if group_list:
        for group_id in group_list:
            #  获取组对象
            try:
                group = Group.query.filter_by(id=group_id).one()
            except Exception as e:
                current_app.logger.error("[group][get] fail expection: {}".format(e))
                raise InvalidMessage(str(e), 500)
            # 添加组给用户
            try:
                user_helper.add_group_to_user(user, group)
            except Exception as e:
                current_app.logger.error("[user][add_group] fail expection: {}".format(e))
                raise InvalidMessage(str(e), 500)
    db.session.commit()
    data = user_helper.make_user_reponse_body(user)
    return return_data(data, 201)


@auth.route('/delete_user/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_user(id):
    # 获取用户对象
    try:
        user = user_datastore.find_user(id=id)
    except Exception as e:
        current_app.logger.error("[user][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    # 从用户中移除所有组
    try:
        user_helper.remove_all_group_to_user(user)
    except Exception as e:
        current_app.logger.error("[user][remove_all_group] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    # 删除用户
    try:
        user_datastore.delete_user(user)
    except Exception as e:
        current_app.logger.error("[user][del] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    db.session.commit()
    return return_data('delete success', 204)


@auth.route('/update_user/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_user(id):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    if "password" in args:
        args['password'] = hash_password(args['password'])
    try:
        com_put(db, User, args, **{'id': id})
    except Exception as e:
        current_app.logger.error("[user][put] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    return return_data('update success', 200)


@auth.route('/get_user/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_user(id):
    try:
        user = com_get(User, id=id)
    except Exception as e:
        current_app.logger.error("[user][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    data = user_helper.make_user_reponse_body(user)
    return return_data(data, 200)


@auth.route('/get_users', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_users():
    try:
        users = com_gets(User)
    except Exception as e:
        current_app.logger.error("[user][gets] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    datas = []
    for user in users:
        data = user_helper.make_user_reponse_body(user)
        datas.append(data)
    return return_data(datas, 200)


@auth.route('/create_group', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_group():
    try:
        group = com_post(db, Group)
    except Exception as e:
        current_app.logger.error("[group][post] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    data = user_helper.make_group_reponse_body(group)
    return return_data(data, 201)


@auth.route('/update_group/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_group(id):
    try:
        com_put(db, Group, **{'id': id})
    except Exception as e:
        current_app.logger.error("[group][put] fail expection: {}".format(e))
    return return_data('update success', 200)


@auth.route('/delete_group/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_group(id):
    # 获取组对象
    try:
        group = com_get(Group, id=id)
    except Exception as e:
        current_app.logger.error("[group][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    # 从组中移除所有用户
    try:
        user_helper.remove_all_user_to_group(group)
    except Exception as e:
        current_app.logger.error("[group][remove_all_user] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    # 删除组
    try:
        com_del(db, Group, id=id)
    except Exception as e:
        current_app.logger.error("[group][del] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@auth.route('/add_group_to_user', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def add_group_to_user():
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    user_id = args['user_id']
    group_ids = args['groups']
    # 获取用户对象
    try:
        user = com_get(User, id=user_id)
    except Exception as e:
        current_app.logger.error("[user][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    for group_id in group_ids:
        # 获取组对象
        try:
            group = com_get(Group, id=group_id)
        except Exception as e:
            current_app.logger.error("[group][get] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
        # 添加组给用户
        try:
            user_helper.add_group_to_user(user, group)
        except Exception as e:
            current_app.logger.error("[user][add_group] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
    db.session.commit()
    return return_data('update success', 200)


@auth.route('/remove_group_to_user', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def remove_group_to_user():
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    user_id = args['user_id']
    group_ids = args['groups']
    try:
        user = com_get(User, id=user_id)
    except Exception as e:
        current_app.logger.error("[user][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    for group_id in group_ids:
        try:
            group = com_get(Group, id=group_id)
        except Exception as e:
            current_app.logger.error("[group][get] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
        try:
            user_helper.remove_group_to_user(user, group)
        except Exception as e:
            current_app.logger.error("[user][remove_group] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
    db.session.commit()
    return return_data('update success', 200)


@auth.route('/get_groups', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_groups():
    try:
        groups = com_gets(Group)
    except Exception as e:
        current_app.logger.error("[group][gets] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    datas = []
    for group in groups:
        data = user_helper.make_role_reponse_body(group)
        datas.append(data)
    return return_data(datas, 200)


@auth.route('/get_group/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_group(id):
    try:
        group = com_get(Group, id=id)
    except Exception as e:
        current_app.logger.error("[group][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    data = user_helper.make_role_reponse_body(group)
    return return_data(data, 200)


@auth.route('/add_role_to_user', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def add_role_to_user():
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    user_id = args['user_id']
    role_ids = args['roles']
    try:
        user = user_datastore.find_user(id=user_id)
    except Exception as e:
        current_app.logger.error("[user][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    for role_id in role_ids:
        try:
            role = com_get(Role, id=role_id)
        except Exception as e:
            current_app.logger.error("[role][get] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
        try:
            user_datastore.add_role_to_user(user, role)
        except Exception as e:
            current_app.logger.error("[user][add_role] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
    db.session.commit()
    return return_data('update success', 200)


@auth.route('/remove_role_from_user', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def remove_role_from_user():
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    user_id = args['user_id']
    role_ids = args['roles']
    try:
        user = user_datastore.find_user(id=user_id)
    except Exception as e:
        current_app.logger.error("[user][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    for role_id in role_ids:
        try:
            role = com_get(Role, id=role_id)
        except Exception as e:
            current_app.logger.error("[role][get] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
        try:
            user_datastore.remove_role_from_user(user, role)
        except Exception as e:
            current_app.logger.error("[user][remove_role] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
    db.session.commit()
    return return_data('update success', 200)


@auth.route('/get_role/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_role(id):
    try:
        role = com_get(Role, id=id)
    except Exception as e:
        current_app.logger.error("[role][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    data = user_helper.make_role_reponse_body(role)
    return return_data(data, 200)


@auth.route('/get_roles', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_roles():
    try:
        roles = com_gets(Role)
    except Exception as e:
        current_app.logger.error("[role][gets] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    datas = []
    for role in roles:
        data = user_helper.make_role_reponse_body(role)
        datas.append(data)
    return return_data(datas, 200)


@auth.route('/update_role/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_role(id):
    try:
        com_put(db, Role, **{'id': id})
    except Exception as e:
        current_app.logger.error("[role][put] fail expection: {}".format(e))
    return return_data('update success', 200)