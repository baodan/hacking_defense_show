from app.urls import exam
from flask import current_app, request
from flask_security import auth_token_required
from flask_security import roles_accepted, roles_required
from tools.common_restful import com_put, com_post, com_del,\
    com_get, com_gets
from app.database import db
from app.customer_error_class import InvalidMessage
from app.return_format import return_data
from app.models.answer import Scene, Subject, Paper,\
    Question, Head, Label
from tools import model_helper


@exam.route('/create_label', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_label():
    try:
        label = com_post(db, Label)
    except Exception as e:
        current_app.logger.error("[label][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(label)
    return return_data(data, 201)


@exam.route('/update_label/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_label(id):
    try:
        com_put(db, Label, **{'id': id})
    except Exception as e:
        current_app.logger.error("[label][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@exam.route('/delete_label/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_label(id):
    # 数据头需为json格式
    if request.labelers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, Label, id=id)
    except Exception as e:
        current_app.logger.error("[label][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@exam.route('/get_labels', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_labels():
    try:
        labels = com_gets(Label)
    except Exception as e:
        current_app.logger.error("[label][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(labels)
    return return_data(datas, 200)


@exam.route('/get_label/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_label(id):
    try:
        label = com_get(Label, id=id)
    except Exception as e:
        current_app.logger.error("[label][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(label)
    return return_data(data, 200)


@exam.route('/create_head', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_head():
    try:
        head = com_post(db, Head)
    except Exception as e:
        current_app.logger.error("[head][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(head)
    return return_data(data, 201)


@exam.route('/update_head/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_head(id):
    try:
        com_put(db, Head, **{'id': id})
    except Exception as e:
        current_app.logger.error("[head][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@exam.route('/delete_head/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_head(id):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, Head, id=id)
    except Exception as e:
        current_app.logger.error("[head][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@exam.route('/get_heads', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_heads():
    try:
        heads = com_gets(Head)
    except Exception as e:
        current_app.logger.error("[head][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(heads)
    return return_data(datas, 200)


@exam.route('/get_head/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_head(id):
    try:
        head = com_get(Head, id=id)
    except Exception as e:
        current_app.logger.error("[head][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(head)
    return return_data(data, 200)


@exam.route('/create_scene', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_scene():
    try:
        scene = com_post(db, Scene)
    except Exception as e:
        current_app.logger.error("[scene][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(scene)
    return return_data(data, 201)


@exam.route('/update_scene/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_scene(id):
    try:
        com_put(db, Scene, **{'id': id})
    except Exception as e:
        current_app.logger.error("[scene][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@exam.route('/delete_scene/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_scene(id):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, Scene, id=id)
    except Exception as e:
        current_app.logger.error("[scene][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@exam.route('/get_scenes', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_scenes():
    try:
        scenes = com_gets(Scene)
    except Exception as e:
        current_app.logger.error("[scene][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(scenes)
    return return_data(datas, 200)


@exam.route('/get_scene/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_scene(id):
    try:
        scene = com_get(Scene, id=id)
    except Exception as e:
        current_app.logger.error("[scene][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(scene)
    return return_data(data, 200)


@exam.route('/create_subject', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_subject():
    try:
        subject = com_post(db, Subject)
    except Exception as e:
        current_app.logger.error("[subject][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(subject)
    return return_data(data, 201)


@exam.route('/update_subject/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_subject(id):
    try:
        com_put(db, Subject, **{'id': id})
    except Exception as e:
        current_app.logger.error("[subject][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@exam.route('/delete_subject/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_subject(id):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, Subject, id=id)
    except Exception as e:
        current_app.logger.error("[subject][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@exam.route('/get_subjects', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_subjects():
    try:
        subjects = com_gets(Subject)
    except Exception as e:
        current_app.logger.error("[subject][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(subjects)
    return return_data(datas, 200)


@exam.route('/get_subject/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_subject(id):
    try:
        subject = com_get(Subject, id=id)
    except Exception as e:
        current_app.logger.error("[subject][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(subject)
    return return_data(data, 200)


@exam.route('/create_paper', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_paper():
    try:
        paper = com_post(db, Paper)
    except Exception as e:
        current_app.logger.error("[paper][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(paper)
    return return_data(data, 201)


@exam.route('/update_paper/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_paper(id):
    try:
        com_put(db, Paper, **{'id': id})
    except Exception as e:
        current_app.logger.error("[paper][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@exam.route('/delete_paper/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_paper(id):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, Paper, id=id)
    except Exception as e:
        current_app.logger.error("[paper][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@exam.route('/get_papers', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_papers():
    try:
        papers = com_gets(Paper)
    except Exception as e:
        current_app.logger.error("[paper][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(papers)
    return return_data(datas, 200)


@exam.route('/get_paper/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_paper(id):
    try:
        paper = com_get(Paper, id=id)
    except Exception as e:
        current_app.logger.error("[paper][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(paper)
    return return_data(data, 200)


@exam.route('/create_question', methods=['POST'])
@roles_required('admin')
@auth_token_required
def create_question():
    try:
        question = com_post(db, Question)
    except Exception as e:
        current_app.logger.error("[question][post] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(question)
    return return_data(data, 201)


@exam.route('/update_question/<int:id>', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def update_question(id):
    try:
        com_put(db, Question, **{'id': id})
    except Exception as e:
        current_app.logger.error("[question][put] fail expection: {}".format(e))
    
    return return_data('update success', 200)


@exam.route('/delete_question/<int:id>', methods=['DELETE'])
@roles_required('admin')
@auth_token_required
def delete_question(id):
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    # 删除场景
    try:
        com_del(db, Question, id=id)
    except Exception as e:
        current_app.logger.error("[question][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@exam.route('/get_questions', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_questions():
    try:
        questions = com_gets(Question)
    except Exception as e:
        current_app.logger.error("[question][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = model_helper.obj_list_to_list_dict(questions)
    return return_data(datas, 200)


@exam.route('/get_question/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def get_question(id):
    try:
        question = com_get(Question, id=id)
    except Exception as e:
        current_app.logger.error("[question][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(question)
    return return_data(data, 200)