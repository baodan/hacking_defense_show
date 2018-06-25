#!/usr/bin/env python
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
import app.error_class
from app import create_app, db
from app.models.user import User, Role, Group
from app.models.answer import Scene, Subject, Paper,\
    Question, UserPaper, PaperQuestion, UserHead, GroupHead,\
    ApproveLog, PaperQuestionLog

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
models = {
    'User': User,
    'Role': Role,
    'Group': Group,
    'Scene': Scene,
    'Subject': Subject,
    'Paper': Paper,
    'Question': Question,
    'UserPaper': UserPaper,
    'PaperQuestion': PaperQuestion,
    'UserHead': UserHead,
    'GroupHead': GroupHead,
    'ApproveLog': ApproveLog,
    'PaperQuestionLog': PaperQuestionLog
}


def make_shell_context():
    return dict(app=app, db=db, **models)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
