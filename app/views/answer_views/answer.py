from app.urls import answers
from flask import current_app, request
from flask_security import auth_token_required
from flask_security import roles_accepted, roles_required
from tools.common_restful import com_put, com_post, com_del,\
    com_get, com_gets
from app.database import db
from app.customer_error_class import InvalidMessage
from app.return_format import return_data
from app.models.answer import PaperQuestion, UserPaper, GroupHead,\
    UserHead
from tools import model_helper


@answers.route('/create_user_paper', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_user_paper():
    try:
        user_paper = com_post(db, UserPaper)
    except Exception as e:
        current_app.logger.error("[user_paper][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(user_paper)
    return return_data(data, 201)


@answers.route('/update_user_paper/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_user_paper(id):
    try:
        com_put(db, UserPaper, **{'id': id})
    except Exception as e:
        current_app.logger.error("[user_paper][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@answers.route('/delete_user_paper/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_user_paper(id):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, UserPaper, id=id)
    except Exception as e:
        current_app.logger.error("[user_paper][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@answers.route('/get_user_papers', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_user_papers():
    try:
        user_papers = com_gets(UserPaper)
    except Exception as e:
        current_app.logger.error("[user_paper][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(user_papers)
    return return_data(datas, 200)


@answers.route('/get_user_paper/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_user_paper(id):
    try:
        user_paper = com_get(UserPaper, id=id)
    except Exception as e:
        current_app.logger.error("[user_paper][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(user_paper)
    return return_data(data, 200)


@answers.route('/create_paper_question', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_paper_question():
    try:
        paper_question = com_post(db, PaperQuestion)
    except Exception as e:
        current_app.logger.error("[paper_question][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(paper_question)
    return return_data(data, 201)


@answers.route('/update_paper_question/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_paper_question(id):
    try:
        com_put(db, PaperQuestion, **{'id': id})
    except Exception as e:
        current_app.logger.error("[paper_question][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@answers.route('/delete_paper_question/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_paper_question(id):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, PaperQuestion, id=id)
    except Exception as e:
        current_app.logger.error("[paper_question][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@answers.route('/get_paper_questions', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_paper_questions():
    try:
        paper_questions = com_gets(PaperQuestion)
    except Exception as e:
        current_app.logger.error("[paper_question][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(paper_questions)
    return return_data(datas, 200)


@answers.route('/get_paper_question/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_paper_question(id):
    try:
        paper_question = com_get(PaperQuestion, id=id)
    except Exception as e:
        current_app.logger.error("[paper_question][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(paper_question)
    return return_data(data, 200)


@answers.route('/create_group_head', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_group_head():
    try:
        group_head = com_post(db, GroupHead)
    except Exception as e:
        current_app.logger.error("[group_head][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(group_head)
    return return_data(data, 201)


@answers.route('/update_group_head/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_group_head(id):
    try:
        com_put(db, GroupHead, **{'id': id})
    except Exception as e:
        current_app.logger.error("[group_head][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@answers.route('/delete_group_head/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_group_head(id):
    # 数据头需为json格式
    if request.group_headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, GroupHead, id=id)
    except Exception as e:
        current_app.logger.error("[group_head][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@answers.route('/get_group_heads', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_group_heads():
    try:
        group_heads = com_gets(GroupHead)
    except Exception as e:
        current_app.logger.error("[group_head][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(group_heads)
    return return_data(datas, 200)


@answers.route('/get_group_head/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_group_head(id):
    try:
        group_head = com_get(GroupHead, id=id)
    except Exception as e:
        current_app.logger.error("[group_head][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(group_head)
    return return_data(data, 200)


@answers.route('/create_user_head', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_user_head():
    try:
        user_head = com_post(db, UserHead)
    except Exception as e:
        current_app.logger.error("[user_head][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(user_head)
    return return_data(data, 201)


@answers.route('/update_user_head/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_user_head(id):
    try:
        com_put(db, UserHead, **{'id': id})
    except Exception as e:
        current_app.logger.error("[user_head][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@answers.route('/delete_user_head/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_user_head(id):
    # 数据头需为json格式
    if request.user_headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, UserHead, id=id)
    except Exception as e:
        current_app.logger.error("[user_head][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@answers.route('/get_user_heads', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_user_heads():
    try:
        user_heads = com_gets(UserHead)
    except Exception as e:
        current_app.logger.error("[user_head][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(user_heads)
    return return_data(datas, 200)


@answers.route('/get_user_head/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_user_head(id):
    try:
        user_head = com_get(UserHead, id=id)
    except Exception as e:
        current_app.logger.error("[user_head][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(user_head)
    return return_data(data, 200)



