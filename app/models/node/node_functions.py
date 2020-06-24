from app import app, rc
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict


def get_all_nodes(ses, node_model):
    try:
        data = ses.query(node_model).all()
    except NoResultFound:
        return False, None
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict
    else:
        return False, None


def get_node_by_node_id(ses, node_model, node_id):
    try:
        data = ses.query(node_model).filter_by(node_id=node_id).one()
    except NoResultFound:
        return False, None
    dict_node = data.to_dict()

    if len(dict_node) > 0:
        return True, dict_node
    else:
        return False, None


def del_node_by_node_id(ses, node_model, node_id):
    try:
        data = ses.query(node_model).filter_by(node_id=node_id).one()
        ses.query(node_model).filter_by(node_id=node_id).delete()
    except NoResultFound:
        return False, None, "node not found"

    dict_node = data.to_dict()

    if len(dict_node) > 0:
        return True, dict_node, None
    else:
        return False, None, None
