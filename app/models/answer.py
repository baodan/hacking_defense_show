from app.database import db
from model_base import BaseModel


labels_subjects = db.Table('labels_subjects',
        db.Column('label_id', db.Integer(), db.ForeignKey('label.id')),
        db.Column('subject_id', db.Integer(), db.ForeignKey('subject.id')))

groups_heads = db.Table('groups_heads',
                         db.Column('group_id', db.Integer(), db.ForeignKey('group.id')),
                         db.Column('head_id', db.Integer(), db.ForeignKey('head.id')))

users_papers = db.Table('users_papers',
                         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                         db.Column('paper_id', db.Integer(), db.ForeignKey('paper.id')))


class Scene(BaseModel):
    __tablename__ = 'scene'
    describe = db.Column(db.Text, comment='场景描述')


class Label(BaseModel):
    __tablename__ = 'label'
    name = db.Column(db.String(255), comment='标签简述')
    describe = db.Column(db.Text, comment='标签描述')


class Subject(BaseModel):
    __tablename__ = 'subject'
    topic = db.Column(db.Text, comment='考题题目')
    type = db.Column(db.String(255), comment='考题类型')
    answer = db.Column(db.Text, comment='考题答案')
    scene_id = db.Column(db.Integer, db.ForeignKey('scene.id'),
                             comment='场景id')
    scene = db.relationship('Scene',
                                 backref=db.backref('subject',
                                                    lazy='dynamic'))
    labels = db.relationship('Label', secondary=labels_subjects,
                            backref=db.backref('subjects', lazy='dynamic'))


class Head(BaseModel):
    __tablename__ = 'head'
    name = db.Column(db.String(255), comment='标题')
    all_score = db.Column(db.Integer, comment='总分')
    groups = db.relationship('Group', secondary=groups_heads,
                            backref=db.backref('heads', lazy='dynamic'))
    

class Paper(BaseModel):
    __tablename__ = 'paper'
    name = db.Column(db.String(255), comment='考试名称')
    total_paper_score = db.Column(db.Integer, comment='考卷总分')
    exam_time = db.Column(db.Integer, comment='考试时间（分钟）')
    remainder_time = db.Column(db.Integer, comment='剩余时间（分钟）')
    head_id = db.Column(db.Integer, db.ForeignKey('head.id'),
                             comment='标题')
    head = db.relationship('Head',
                                 backref=db.backref('papers',
                                                    lazy='dynamic'))
    status = db.Column(db.String(255), comment='状态', default='new')
    users = db.relationship('User', secondary=users_papers,
                            backref=db.backref('papers', lazy='dynamic'))
    
    
class Question(BaseModel):
    __tablename__ = 'question'
    number = db.Column(db.Integer, comment='题号')
    total_question_score = db.Column(db.Integer, comment='考题总分')
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'),
                             comment='题目id')
    subject = db.relationship('Subject',
                                 backref=db.backref('question',
                                                    lazy='dynamic'))
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'),
                             comment='考卷id')
    paper = db.relationship('Paper',
                                 backref=db.backref('questions',
                                                    lazy='dynamic', order_by=number))


class GroupHead(BaseModel):
    __tablename__ = 'group_head'
    total_group_score = db.Column(db.Integer, comment='组总得分', default=0)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'),
                             comment='用户')
    head_id = db.Column(db.Integer, db.ForeignKey('head.id'),
                             comment='标题')
    head = db.relationship('Head',
                                 backref=db.backref('group_head',
                                                    lazy='dynamic'))
    group = db.relationship('Group',
                                 backref=db.backref('group_head',
                                                    lazy='dynamic'))


class UserHead(BaseModel):
    __tablename__ = 'user_head'
    total_user_score = db.Column(db.Integer, comment='用户总得分', default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                             comment='用户')
    user = db.relationship('User',
                                 backref=db.backref('user_head',
                                                    lazy='dynamic'))
    head_id = db.Column(db.Integer, db.ForeignKey('head.id'),
                             comment='标题')
    head = db.relationship('Head',
                                 backref=db.backref('user_head',
                                                    lazy='dynamic'))
    group_head_id = db.Column(db.Integer, db.ForeignKey('group_head.id'),
                             comment='组标题id')
    group_head = db.relationship('GroupHead',
                                 backref=db.backref('user_heads',
                                                    lazy='dynamic'))
    
    
class UserPaper(BaseModel):
    __tablename__ = 'user_paper'
    user_score = db.Column(db.Integer, comment='考卷得分', default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                             comment='用户')
    user = db.relationship('User',
                                 backref=db.backref('user_paper',
                                                    lazy='dynamic'))
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'),
                             comment='考卷id')
    paper = db.relationship('Paper',
                                 backref=db.backref('user_paper',
                                                    lazy='dynamic'))
    user_head_id = db.Column(db.Integer, db.ForeignKey('user_head.id'),
                             comment='用户标题id')
    user_head = db.relationship('UserHead',
                                 backref=db.backref('user_papers',
                                                    lazy='dynamic'))

    
class PaperQuestion(BaseModel):
    __tablename__ = 'paper_question'
    question_score = db.Column(db.Integer, comment='考题得分', default=0)
    user_paper_id = db.Column(db.Integer, db.ForeignKey('user_paper.id'),
                             comment='用户的考卷')
    user_answer = db.Column(db.Text, comment='用户答案')
    user_paper = db.relationship('UserPaper',
                                 backref=db.backref('paper_questions',
                                                    lazy='dynamic'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
                             comment='关联的考题')
    question = db.relationship('Question',
                                 backref=db.backref('paper_questions',
                                                    lazy='dynamic'))
    status = db.Column(db.String(255), comment='状态', default='uncommitted')


class PaperQuestionLog(BaseModel):
    __tablename__ = 'paper_question_log'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                             comment='用户')
    context = db.Column(db.Text, comment='用户答案')
    paper_question_id = db.Column(db.Integer, db.ForeignKey('paper_question.id'),
                             comment='考题')


class ApproveLog(BaseModel):
    __tablename__ = 'approve_log'
    examiner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                             comment='考官')
    question_score = db.Column(db.Integer, comment='考题得分')
    context = db.Column(db.Text, comment='用户答案')
    paper_question_id = db.Column(db.Integer, db.ForeignKey('paper_question.id'),
                             comment='考题')
