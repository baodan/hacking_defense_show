from app.database import db, app
from config import config
from logger_setting import server_log
from app.models.user import User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from app.urls import auth, exam, answers


# 可以直接把对象里面的配置数据转换到app.config里面
app.config.from_object(config['development'])


def create_app():
    """Creates a app.
    :returns: app
    """
    # 设置日志
    app.logger.addHandler(server_log)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(exam, url_prefix='/exam')
    app.register_blueprint(answers, url_prefix='/answers')
    # app.logger.addHandler(error_log)
    # 注册 Flask-SQLAlchemy
    # 这个对象在其他地方想要使用
    # SQLAlchemy(app)
    db.init_app(app)
    return app


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def create_user():
    if not User.query.first():
        user = user_datastore.create_user(username='admin', password=hash_password('Ad@min2018'))
    if not Role.query.first():
        admin = user_datastore.create_role(name="admin", description="管理员")
        examiner = user_datastore.create_role(name="examiner", description="考官")
        contestant = user_datastore.create_role(name="contestant", description="参赛者")
        user_datastore.add_role_to_user(user, admin)
        db.session.commit()


