from app.database import db
from model_base import BaseModel
from flask_security import UserMixin, RoleMixin

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

groups_users = db.Table('groups_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('group_id', db.Integer(), db.ForeignKey('group.id')))


class Role(BaseModel, RoleMixin):
    __tablename__ = 'role'
    name = db.Column(db.String(255), unique=True, index=True)
    description = db.Column(db.String(255), index=True)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    username = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), index=True)
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(63))
    current_login_ip = db.Column(db.String(63))
    login_count = db.Column(db.Integer)
    groups = db.relationship('Group', secondary=groups_users,
                            backref=db.backref('users', lazy='dynamic'))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return '<User %r>' % self.username
    

class Group(BaseModel):
    __tablename__ = 'group'
    name = db.Column(db.String(255), unique=True, index=True)
    description = db.Column(db.Text(), index=True)

