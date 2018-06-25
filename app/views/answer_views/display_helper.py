def make_group_head_reponse_body(group_head):
    data = {
        'group_head': {
            'id': group_head.id,
            'total_group_score': group_head.total_group_score,
            'group_id': group_head.group_id
        },
        'user_heads': [],
        'group': {}
    }
    group = group_head.group
    user_heads = group_head.user_heads
    if group:
        data['group'] = {
            'id': group.id,
            'name': group.name,
            'all_score': group.all_score
        }
    if user_heads:
        for user_head in user_heads:
            user_head = {
                'id': user_head.id,
                'user': {},
                'head': {},
                'total_user_score': user_head.total_user_score,
                'user_papers': []
            }
            user = user_head.user
            head = user_head.head
            user_papers = user_head.user_papers
            data['user_heads'].append(user_head)
            if user:
                user_head['user'] = {
                    'id': user.id,
                    'username': user.username
                }
            if head:
                user_head['head'] = {
                    'id': head.id,
                    'name': head.name,
                    'all_score': head.all_score
                }
            if user_papers:
                for user_paper in user_papers:
                    user_paper = {
                        'id': user_paper.id,
                        'user_score': user_paper.user_score,
                        'paper': {}
                    }
                    paper = user_paper.paper
                    if paper:
                        user_paper['paper'] = {
                            'id': paper.id,
                            'name': paper.name,
                            'total_paper_score': paper.total_paper_score,
                            'exam_time': paper.exam_time,
                            'remainder_time': paper.remainder_time
                        }
            data['user_heads'].append(user_head)
            
    return data