from app.database import db
from app.models.user import Group


def add_group_to_user(user, group):
    user.groups.append(group)
    

def remove_group_to_user(user, group):
    user.groups.remove(group)
    
    
def remove_all_group_to_user(user):
    user.groups = []


def remove_all_user_to_group(group):
    group.users = []


def make_user_reponse_body(user):
    data = {
        'user': {
            'id': user.id,
            'username': user.username,
            'active': user.active,
            'confirmed_at': user.confirmed_at,
            'last_login_at': user.last_login_at,
            'current_login_at': user.current_login_at,
            'last_login_ip': user.last_login_ip,
            'current_login_ip': user.current_login_ip,
            'login_count': user.login_count,
        },
        'groups': [],
        'roles': []
    }
    groups = user.groups
    roles = user.roles
    if groups:
        for group in groups:
            data['groups'].append(make_group_reponse_body(group))
    if roles:
        for role in roles:
            data['roles'].append(make_group_reponse_body(role))
    return data


def make_role_reponse_body(role):
    data = {
        'id': role.id,
        'name': role.name,
        'description': role.description
    }
    return data


def make_group_reponse_body(group):
    data = {
        'id': group.id,
        'name': group.name,
        'description': group.description
    }
    return data
