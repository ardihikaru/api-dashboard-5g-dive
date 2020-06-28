from app import app, rc, local_settings
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict
from app.addons.cryptography.fernet import encrypt


def insert_new_data(ses, data_model, new_data):
    new_data["identifier"] = encrypt(new_data["node_name"])
    ses.add(data_model(
                node_id=new_data["node_id"],
                node_name=new_data["node_name"],
                identifier=new_data["identifier"]
            )
    )

    _, inserted_data = get_data_by_identifier(ses, data_model, new_data["identifier"])

    if len(inserted_data) > 0:
        return True, inserted_data
    else:
        return False, None


def get_data_by_identifier(ses, data_model, identifier):
    try:
        data = ses.query(data_model).filter_by(identifier=identifier).one()
    except NoResultFound:
        return False, None
    dict_data = data.to_dict()

    if len(dict_data) > 0:
        return True, dict_data
    else:
        return False, None


def get_all_nodes(ses, node_model, args=None):
    try:
        if args is not None:
            if len(args["range"]) == 0:
                args["range"] = [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]]
        else:
            args = {
                "filter": {},
                "range": [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]],
                "sort": []
            }
        data = ses.query(node_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except NoResultFound:
        return False, None
    # except Exception as e:
    #     print(" -- e:", e)
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


def del_all_nodes(ses, node_model):
    try:
        data = ses.query(node_model).all()
        ses.query(node_model).delete()
    except NoResultFound:
        return False, None, "node not found"

    dict_node = sqlresp_to_dict(data)

    if len(dict_node) > 0:
        return True, dict_node, None
    else:
        return False, None, None


def upd_data_by_id(ses, data_model, uid, new_data=None):
    try:
        data = ses.query(data_model).filter_by(id=uid).one()

        if new_data is not None:
            data.node_id = new_data["node_id"] if "node_id" in new_data else data.node_id
            data.node_name = new_data["node_name"] if "node_name" in new_data else data.node_name

        ses.query(data_model).filter_by(id=uid).update(
            {
                "node_id": data.node_id,
                "node_name": data.node_name
            }
        )
    except NoResultFound:
        return False, None, None
    dict_data = data.to_dict()

    if len(dict_data) > 0:
        return True, dict_data, None
    else:
        return False, None, None


def get_data_by_uid(ses, data_model, uid):
    try:
        data = ses.query(data_model).filter_by(id=uid).one()
    except NoResultFound:
        return False, None
    dict_data = data.to_dict()

    if len(dict_data) > 0:
        return True, dict_data
    else:
        return False, None


def del_data_by_id(ses, data_model, uid):
    try:
        data = ses.query(data_model).filter_by(id=uid).one()
        ses.query(data_model).filter_by(id=uid).delete()
    except NoResultFound:
        return False, None, "node not found"

    dict_data = data.to_dict()

    if len(dict_data) > 0:
        return True, dict_data, None
    else:
        return False, None, None

