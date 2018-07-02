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
    Question, Head, Label, GroupHead, UserHead, UserPaper,\
    PaperQuestion
from tools import model_helper
from app.views.answer_views import paper_helper
import threading
import time


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
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    subject_dict = args.get('subject', '')
    label_list = args.get('labels', '')
    try:
        # 获取post内容
        subject = Subject(**subject_dict)
    except Exception as e:
        current_app.logger.error("{} model init exception: {}".format(Subject, e))
        current_app.logger.error("model_data: {}".format(subject_dict))
        raise e
    if label_list:
        for label_id in label_list:
            #  获取标签对象
            try:
                label = Label.query.filter_by(id=label_id).one()
            except Exception as e:
                current_app.logger.error("[label][get] fail expection: {}".format(e))
                raise InvalidMessage(str(e), 500)
            # 添加标签给题
            try:
                paper_helper.add_label_to_subject(subject, label)
            except Exception as e:
                current_app.logger.error("[user][add_group] fail expection: {}".format(e))
                raise InvalidMessage(str(e), 500)
    # 添加对象
    db.session.add(subject)
    try:
        # 同步数据到数据库
        db.session.commit()
    except Exception as e:
        current_app.logger.error("{} model init exception: {}".format(Subject, e))
        current_app.logger.error("model_data: {}".format(args))
        raise e
    data = paper_helper.make_subject_reponse_body(subject)
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
    datas = []
    for subject in subjects:
        data = paper_helper.make_subject_reponse_body(subject)
        datas.append(data)
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
    data = paper_helper.make_subject_reponse_body(subject)
    return return_data(data, 200)


@exam.route('/add_label_to_subject', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def add_label_to_subject():
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    subject_id = args['subject_id']
    label_ids = args['labels']
    # 获取题对象
    try:
        subject = com_get(Subject, id=subject_id)
    except Exception as e:
        current_app.logger.error("[subject][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    for label_id in label_ids:
        # 获取标签对象
        try:
            label = com_get(Label, id=label_id)
        except Exception as e:
            current_app.logger.error("[label][get] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
        # 添加组给用户
        try:
            paper_helper.add_label_to_subject(subject, label)
        except Exception as e:
            current_app.logger.error("[label][add_label] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
    db.session.commit()
    return return_data('update success', 200)


@exam.route('/remove_label_to_subject', methods=['PUT'])
@roles_required('admin')
@auth_token_required
def remove_label_to_subject():
    # 数据头需为json格式
    if request.headers['Content-Type'] == 'application/json':
        args = request.json
        current_app.logger.debug('get_token args: {}'.format(args))
    else:
        raise InvalidMessage('only support json data', 404)
    subject_id = args['subject_id']
    label_ids = args['labels']
    # 获取题对象
    try:
        subject = com_get(Subject, id=subject_id)
    except Exception as e:
        current_app.logger.error("[subject][get] fail expection: {}".format(e))
        raise InvalidMessage(str(e), 500)
    for label_id in label_ids:
        # 获取标签对象
        try:
            label = com_get(Label, id=label_id)
        except Exception as e:
            current_app.logger.error("[label][get] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
        try:
            paper_helper.remove_label_to_subject(subject, label)
        except Exception as e:
            current_app.logger.error("[subject][remove_label] fail expection: {}".format(e))
            raise InvalidMessage(str(e), 500)
    db.session.commit()
    return return_data('update success', 200)


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
        questions = Question.query.order_by('number')
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


@exam.route('/start_paper/<int:id>', methods=['PUT'])
@roles_required('examiner')
@auth_token_required
def start_paper(id):
    try:
        # 查询数据
        paper = Paper.query.filter_by(id=id).one()
        paper.status = "going"
    except Exception as e:
        current_app.logger.error("{} key=value filter_by exception: {}".format(Paper, e))
        current_app.logger.error("key=value filter_by: {}".format(id))
        raise e
    head = paper.head
    groups = head.groups
    users = paper.users
    questions = paper.questions
    # 如果这是第一个paper创建所有group_head
    if groups and not head.user_heads:
        for group in groups:
            group_head_dict = {
                'head_id': head.id,
                'group_id': group.id
            }
            group_head = GroupHead(**group_head_dict)
    else:
        return return_data('no group to exam', 404)
    if users:
        for user in users:
            user_groups = user.groups
            inter_group_list = list(set(user_groups) & set(groups))
            # 在一次paper中一个user只能属于一个group
            if len(inter_group_list) == 1:
                try:
                    # 找到这次paper中这个user的唯一组，一般存在
                    group_head = GroupHead.query.filter_by(group_id=inter_group_list[0].id, head_id=head.id).one_or_none()
                except Exception as e:
                    current_app.logger.error("{} key=value filter_by exception: {}".format(GroupHead, e))
                    current_app.logger.error("key=value filter_by: {}".format(id))
                if group_head:
                    try:
                        # 查找这个用户在这个head是否已经创建user_head
                        user_head = UserHead.query.filter_by(user_id=user.id, head_id=head.id).one_or_none()
                    except Exception as e:
                        current_app.logger.error("{} key=value filter_by exception: {}".format(GroupHead, e))
                        current_app.logger.error("key=value filter_by: {}".format(id))
                    #  若user_head不存在就创建一个
                    if not user_head:
                        user_head_dict = {
                            'user_id': user.id,
                            'head_id': paper.head_id,
                            'group_head_id': group_head.id
                        }
                        user_head = UserHead(**user_head_dict)
                    user_paper_dict = {
                        "user_id": user.id,
                        "paper_id": paper.id,
                        "user_head_id": user_head.id
                    }
                    # 创建user_paper
                    user_paper = UserPaper(**user_paper_dict)
                    # 创建user_paper下的这个user的所有paper_question
                    for question in questions:
                        paper_question_dict = {
                            "user_paper_id": user_paper.id,
                            "question_id": question.id
                        }
                        paper_question = PaperQuestion(**paper_question_dict)
            else:
                return return_data('no group to exam', 404)
    try:
        # 同步数据到数据库
        db.session.commit()
    except Exception as e:
        current_app.logger.error("{} update db commit exception: {}".format(Paper, e))
    t = threading.Thread(target=compute_time, args=(paper,))
    t.start()
    return return_data('paper going', 200)


@exam.route('/end_paper/<int:id>', methods=['PUT'])
@roles_required('examiner')
@auth_token_required
def end_paper(id):
    try:
        # 查询数据
        paper = Paper.query.filter_by(id=id).one()
        paper.status = "close"
    except Exception as e:
        current_app.logger.error("{} key=value filter_by exception: {}".format(Paper, e))
        current_app.logger.error("key=value filter_by: {}".format(id))
        raise e
    try:
        # 同步数据到数据库
        db.session.commit()
    except Exception as e:
        current_app.logger.error("{} update db commit exception: {}".format(Paper, e))
    return return_data('paper close', 200)


def compute_time(paper):
    remainder_time = paper.remainder_time
    while remainder_time:
        time.sleep(60)
        remainder_time = remainder_time - 1
        paper.remainder_time = remainder_time
        try:
            # 同步数据到数据库
            db.session.commit()
        except Exception as e:
            current_app.logger.error("{} update raiming_time exception: {}".format(Paper, e))