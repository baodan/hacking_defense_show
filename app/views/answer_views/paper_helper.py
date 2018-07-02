from app.views.user_views.user_helper import make_group_reponse_body


def add_label_to_subject(subject, label):
    subject.labels.append(label)


def remove_label_to_subject(subject, label):
    subject.labels.remove(label)


def make_subject_reponse_body(subject):
    data = {
        'subject': {
            'id': subject.id,
            'question': subject.question,
            'type': subject.type,
            'answer': subject.answer,
            'scene_id': subject.scene_id,
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


def add_group_to_paper(paper, group):
    paper.groups.append(group)


def remove_group_to_paper(paper, group):
    paper.groups.remove(group)


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
        'users': []
    }
    users = paper.users
    if users:
        for user in users:
            data['users'].append(make_user_reponse_body(user))
    return data


def make_user_reponse_body(user):
    data = {
        'user': {
            'id': user.id,
            'username': user.username,
            'active': user.active
        }
    }
    return data