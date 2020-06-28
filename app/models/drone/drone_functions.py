from app import app, rc, local_settings
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict
from app.addons.cryptography.fernet import encrypt


def insert_new_data(ses, data_model, new_data):
    new_data["identifier"] = encrypt(new_data["drone_name"])
    ses.add(data_model(
        drone_id=new_data["drone_id"],
        drone_name=new_data["drone_name"],
        identifier=new_data["identifier"]
    ))
    _, inserted_data = get_data_by_identifier(ses, data_model, new_data["identifier"])

    if len(inserted_data) > 0:
        return True, inserted_data
    else:
        return False, None


def get_data_by_identifier(ses, data_model, identifier, show_passwd=False):
    try:
        data = ses.query(data_model).filter_by(identifier=identifier).one()
    except NoResultFound:
        return False, None
    dict_user = data.to_dict()

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


def get_all_drones(ses, drone_model, args=None):
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
        data = ses.query(drone_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except NoResultFound:
        return False, None
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict
    else:
        return False, None


def get_drone_by_drone_id(ses, drone_model, drone_id):
    try:
        data = ses.query(drone_model).filter_by(drone_id=drone_id).one()
    except NoResultFound:
        return False, None
    dict_drone = data.to_dict()

    if len(dict_drone) > 0:
        return True, dict_drone
    else:
        return False, None


def del_drone_by_drone_id(ses, drone_model, drone_id):
    try:
        data = ses.query(drone_model).filter_by(drone_id=drone_id).one()
        ses.query(drone_model).filter_by(drone_id=drone_id).delete()
    except NoResultFound:
        return False, None, "drone not found"

    dict_drone = data.to_dict()

    if len(dict_drone) > 0:
        return True, dict_drone, None
    else:
        return False, None, None


def del_all_drones(ses, drone_model):
    try:
        data = ses.query(drone_model).all()
        ses.query(drone_model).delete()
    except NoResultFound:
        return False, None, "node not found"

    dict_drone = sqlresp_to_dict(data)

    if len(dict_drone) > 0:
        return True, dict_drone, None
    else:
        return False, None, None

def upd_data_by_id(ses, data_model, uid, new_data=None):
    try:
        data = ses.query(data_model).filter_by(id=uid).one()

        if new_data is not None:
            data.drone_id = new_data["drone_id"] if "drone_id" in new_data else data.name
            data.drone_name = new_data["drone_name"] if "drone_name" in new_data else data.username

        ses.query(data_model).filter_by(id=uid).update(
            {
                "drone_id": data.drone_id,
                "drone_name": data.drone_name
            }
        )
    except NoResultFound:
        return False, None, None
    dict_data = data.to_dict()

    if len(dict_data) > 0:
        return True, dict_data, None
    else:
        return False, None, None
