from app.views.user_views.user_helper import make_group_reponse_body


def add_group_to_head(head, group):
    head.groups.append(group)


def remove_group_to_head(head, group):
    head.groups.remove(group)


def make_head_reponse_body(head):
    data = {
        'head': {
            'id': head.id,
            'name': head.name,
            'all_score': head.all_score
        },
        'groups': []
    }
    groups = head.groups
    if groups:
        for group in groups:
            data['groups'].append(make_group_reponse_body(group))
    return data


def add_user_to_paper(paper, user):
    paper.users.append(user)


def remove_user_to_paper(paper, user):
    paper.users.remove(user)


def make_paper_reponse_body(paper):
    data = {
        'paper': {
            'id': paper.id,
            'name': paper.name,
            'total_paper_score': paper.total_paper_score,
            'exam_time': paper.exam_time,
            'remainder_time': paper.remainder_time,
            'head_id': paper.head_id,
            'status': paper.status
            
        },
        'users': [],
        'questions': []
    }
    users = paper.users
    questions = paper.questions
    if users:
        for user in users:
            data['users'].append(make_user_reponse_body(user))
    if questions:
        for question in questions:
            data['questions'].append(make_question_reponse_body(question))
    return data


def make_question_reponse_body(question):
    data = {
        'id': question.id,
        'number': question.number,
        'total_question_score': question.total_question_score,
        'paper_id': question.paper_id,
        'subject': make_subject_reponse_body(question.subject)
    }
    return data


def make_user_reponse_body(user):
    data = {
        'id': user.id,
        'username': user.username,
        'active': user.active

    }
    return data


def add_label_to_subject(subject, label):
    subject.labels.append(label)


def remove_label_to_subject(subject, label):
    subject.labels.remove(label)


def make_subject_reponse_body(subject):
    data = {
        'subject': {
            'id': subject.id,
            'type': subject.type,
            'answer': subject.answer,
            'scene_id': subject.scene_id,
            'topic': subject.topic
        },
        'labels': [],
        'scene': {}
    }
    labels = subject.labels
    scene = subject.scene
    if labels:
        for label in labels:
            data['labels'].append(make_label_reponse_body(label))
    if scene:
        data['scene'] = make_scene_reponse_body(scene)
    return data


def make_label_reponse_body(label):
    data = {
        'id': label.id,
        'name': label.name,
        'describe': label.describe
    }
    return data


def make_scene_reponse_body(scene):
    data = {
        'id': scene.id,
        'describe': scene.describe
    }
    return data


def compute_score(head):
    papers = head.papers
    head_score = 0
    for paper in papers:
        paper_score = 0
        questions = paper.questions
        for question in questions:
            paper_score = paper_score + question.total_question_score
        paper.total_paper_score = paper_score
        head_score = head_score + paper_score
    head.all_score = head_score
    
