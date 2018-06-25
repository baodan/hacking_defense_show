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
        'labels': []
    }
    labels = subject.labels
    scenes = subject.scene
    if labels:
        for label in labels:
            data['labels'].append(make_label_reponse_body(label))
    if scenes:
        for scene in scenes:
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

