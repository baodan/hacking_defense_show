from app.views.answer_views.paper_helper import make_question_reponse_body, make_paper_reponse_body
from app.models.answer import PaperQuestion
from app.views.user_views.user_helper import make_user_reponse_body


def compute_score(paper_question):
    group_head = paper_question.user_paper.user_head.group_head
    user_heads = group_head.user_heads
    group_head_score = 0
    for user_head in user_heads:
        user_papers = user_head.user_papers
        user_head_score = 0
        for user_paper in user_papers:
            paper_questions = user_paper.paper_questions
            user_paper_score = 0
            for paper_question in paper_questions:
                user_paper_score = user_paper_score + paper_question.question_score
            user_paper.user_score = user_paper_score
            user_head_score = user_head_score + user_paper_score
        user_head.total_user_score = user_head_score
        group_head_score = group_head_score + user_head_score
    group_head.total_group_score = group_head_score


def make_user_paper_reponse_body(user_paper):
    data = {
        'user_paper': {
            'id': user_paper.id,
            'paper_id': user_paper.paper_id,
            'user_id': user_paper.user_id,
            'user_score': user_paper.user_score,
            'user_head_id': user_paper.user_head_id
        },
        'paper_questions': [],
        'paper': {}
        
    }
    paper_questions = user_paper.paper_questions
    paper = user_paper.paper
    if paper_questions:
        sorted(paper_questions, key=lambda paper_question: paper_question.question.number)
        for paper_question in paper_questions:
            data['paper_questions'].append(make_paper_question_reponse_body(paper_question))
    if paper:
        data['paper'] = make_paper_reponse_body(paper)
    return data


def make_paper_question_reponse_body(paper_question):
    data = {
        'paper_question': {
            'id': paper_question.id,
            'status': paper_question.status,
            'question_score': paper_question.question_score,
            'user_paper_id': paper_question.user_paper_id,
            'user_answer': paper_question.user_answer
        },
        'question': {},
        'user': {}
    }
    question = paper_question.question
    user = paper_question.user_paper.user
    if question:
        data['question'] = make_question_reponse_body(question)
    if user:
        data['user'] = make_user_reponse_body(user)
    return data
