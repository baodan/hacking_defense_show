from app.urls import show
from flask_security import roles_accepted, roles_required
from flask_security import auth_token_required
from app.return_format import return_data
from app.customer_error_class import InvalidMessage
from flask import current_app, request
from app.models.user import Group
from app.models.answer import GroupHead
from tools.common_restful import com_get, com_gets
from app.views.answer_views.display_helper import make_group_head_reponse_body

#id = head.id

@show.route('/show_all_group_score/<int:id>', methods=['GET'])
@roles_required('admin')
@auth_token_required
def show_all_group_score(id):
    groups = Group.query.all()
    datas = []
    if groups:
        for group in groups:
            group_head = GroupHead.query.filter_by(group_id=group.id, head_id=id).one_or_none()
            if group_head:
                group_head_dict = make_group_head_reponse_body(group_head)
                datas.append(group_head_dict)
        #对datas进行排序按照 total_group_score
        sorted(datas, key=lambda data : data['group_head']["total_group_score"], reverse=True)

    return return_data(datas, 200)