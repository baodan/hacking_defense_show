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
    UserHead, Paper, PaperQuestionLog, ApproveLog
from tools import model_helper
from flask_security import current_user
from app.views.answer_views import answer_helper
from sqlalchemy import and_


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
    # 删除场景
    try:
        com_del(db, UserPaper, id=id)
    except Exception as e:
        current_app.logger.error("[user_paper][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@answers.route('/get_user_papers', methods=['GET'])
@roles_accepted('admin', 'examiner', 'contestant')
@auth_token_required
def get_user_papers():
    try:
        user_papers = com_gets(UserPaper)
    except Exception as e:
        current_app.logger.error("[user_paper][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = []
    for user_paper in user_papers:
        data = answer_helper.make_user_paper_reponse_body(user_paper)
        datas.append(data)
    return return_data(datas, 200)


@answers.route('/get_user_paper/<int:id>', methods=['GET'])
@roles_accepted('admin', 'examiner', 'contestant')
@auth_token_required
def get_user_paper(id):
    try:
        user_paper = UserPaper.query.filter(and_(UserPaper.paper.has(Paper.status == "going"),
                                                 UserPaper.user_id == id)).one_or_none()
    except Exception as e:
        current_app.logger.error("[user_paper][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    if user_paper:
        data = answer_helper.make_user_paper_reponse_body(user_paper)
    else:
        data = {}
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
    # 删除场景
    try:
        com_del(db, PaperQuestion, id=id)
    except Exception as e:
        current_app.logger.error("[paper_question][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@answers.route('/get_paper_questions', methods=['GET'])
@roles_accepted('admin', 'examiner', 'contestant')
@auth_token_required
def get_paper_questions():
    try:
        paper_questions = com_gets(PaperQuestion)
    except Exception as e:
        current_app.logger.error("[paper_question][gets] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = []
    for paper_question in paper_questions:
        datas.append(answer_helper.make_paper_question_reponse_body(paper_question))
    return return_data(datas, 200)


@answers.route('/get_paper_question/<int:id>', methods=['GET'])
@roles_accepted('admin', 'examiner', 'contestant')
@auth_token_required
def get_paper_question(id):
    try:
        paper_question = com_get(PaperQuestion, id=id)
    except Exception as e:
        current_app.logger.error("[paper_question][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = answer_helper.make_paper_question_reponse_body(paper_question)
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
    # 删除场景
    try:
        com_del(db, GroupHead, id=id)
    except Exception as e:
        current_app.logger.error("[group_head][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@answers.route('/get_group_heads', methods=['GET'])
@roles_accepted('admin', 'examiner', 'contestant')
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
@roles_accepted('admin', 'examiner', 'contestant')
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
    # 删除场景
    try:
        com_del(db, UserHead, id=id)
    except Exception as e:
        current_app.logger.error("[user_head][del] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    return return_data('delete success', 204)


@answers.route('/get_user_heads', methods=['GET'])
@roles_accepted('admin', 'examiner', 'contestant')
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
@roles_accepted('admin', 'examiner', 'contestant')
@auth_token_required
def get_user_head(id):
    try:
        user_head = com_get(UserHead, id=id)
    except Exception as e:
        current_app.logger.error("[user_head][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    data = model_helper.obj_to_dict(user_head)
    return return_data(data, 200)


@answers.route('/get_deal_paper_questions', methods=['GET'])
@roles_accepted('examiner')
@auth_token_required
def get_deal_paper_questions():
    try:
        paper_questions = PaperQuestion.query.filter(and_(
            PaperQuestion.user_paper.has(UserPaper.paper.has(Paper.status == 'going')),
            PaperQuestion.status == 'pending'
        ))
    except Exception as e:
        current_app.logger.error("[user_head][get] fail expection: {}".format(e))
        return InvalidMessage(str(e), 500)
    datas = []
    for paper_question in paper_questions:
        datas.append(answer_helper.make_paper_question_reponse_body(paper_question))
    return return_data(datas, 200)


@answers.route('/submit_answer/<int:id>', methods=['PUT'])
@roles_required('contestant')
@auth_token_required
def submit_answer(id):
    # 获取post内容
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('submit_answer args: {}'.format(args))
    else:
        raise 'only support json data'
    user_answer = args['user_answer']
    try:
        # 查询数据
        paper_question = PaperQuestion.query.filter_by(id=id).one()
    except Exception as e:
        current_app.logger.error("{} key=value filter_by exception: {}".format(PaperQuestion, e))
        current_app.logger.error("key=value filter_by: {}".format(id))
        raise e
    paper_status = paper_question.question.paper.status
    if paper_status == 'new':
        return return_data('Examination did not begin', 200)
    elif paper_status == 'end':
        return return_data('The exam has ended', 200)

    paper_question.user_answer = user_answer
    paper_question.status = "pending"
    log_dict = {
        'user_id': current_user.id,
        'context': user_answer,
        'paper_question_id': id
    }
    try:
        # 获取post内容
        log = PaperQuestionLog(**log_dict)
    except Exception as e:
        current_app.logger.error("{} model init exception: {}".format(PaperQuestionLog, e))
        current_app.logger.error("model_data: {}".format(log_dict))
        raise e
    try:
        # 同步数据到数据库
        db.session.commit()
    except Exception as e:
        current_app.logger.error("{} update db commit exception: {}".format(Paper, e))
    return return_data('commit success', 200)


@answers.route('/submit_score/<int:id>', methods=['PUT'])
@roles_required('examiner')
@auth_token_required
def submit_score(id):
    # 获取post内容
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('submit_answer args: {}'.format(args))
    else:
        raise 'only support json data'
    question_score = args['question_score']
    try:
        # 查询数据
        paper_question = PaperQuestion.query.filter_by(id=id).one()
        paper_question.question_score = question_score
        paper_question.status = "approved"
    except Exception as e:
        current_app.logger.error("{} key=value filter_by exception: {}".format(PaperQuestion, e))
        current_app.logger.error("key=value filter_by: {}".format(id))
        raise e
    log_dict = {
        'examiner_id': current_user.id,
        'context': paper_question.user_answer,
        'paper_question_id': id,
        'question_score': question_score
    }
    try:
        # 创建日志
        log = ApproveLog(**log_dict)
    except Exception as e:
        current_app.logger.error("{} model init exception: {}".format(ApproveLog, e))
        current_app.logger.error("model_data: {}".format(log_dict))
        raise e
    # 计算分数
    answer_helper.compute_score(paper_question)
    try:
        # 同步数据到数据库
        db.session.commit()
    except Exception as e:
        current_app.logger.error("{} update db commit exception: {}".format(Paper, e))
    return return_data('approval success', 200)



