from flask import Blueprint
exam = Blueprint('exam', __name__)
auth = Blueprint('auth', __name__)
show = Blueprint('show', __name__)
from app.views.user_views import user
from app.views.answer_views import answer
from app.views.answer_views import display