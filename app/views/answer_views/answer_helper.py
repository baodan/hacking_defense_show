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
