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


def get_all_drones(ses, drone_model, args=None):
    try:
        data = None
        if args is not None:
            if len(args["range"]) == 0:
                args["range"] = [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]]
        else:
            args = {
                "filter": {},
                "range": [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]],
                "sort": []
            }
        no_filter = True
        if len(args["filter"]) > 0:
            if "id" in args["filter"]:
                if len(args["filter"]["id"]) == 1:
                    uid = args["filter"]["id"][0]
                    data = ses.query(drone_model).filter_by(id=uid).offset(args["range"][0]).limit(args["range"][1]).all()
                    no_filter = False
        if no_filter:
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


def del_all_drones(ses, drone_model, args=None):
    deleted_data = []
    no_filter = True
    try:
        data = None
        if args is not None:
            if len(args["range"]) == 0:
                args["range"] = [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]]
        else:
            args = {
                "filter": {},
                "range": [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]],
                "sort": []
            }
        if len(args["filter"]) > 0:
            if "id" in args["filter"]:
                for i in range(len(args["filter"]["id"]) ):
                    uid = args["filter"]["id"][i]
                    data = ses.query(drone_model).filter_by(id=uid).one()
                    deleted_data.append(data.to_dict())
                    ses.query(drone_model).filter_by(id=uid).delete()
                    no_filter = False
        if no_filter:
            data = ses.query(drone_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except NoResultFound:
        return False, None, "Drone not found"

    if no_filter:
        dict_drone = sqlresp_to_dict(data)
    else:
        dict_drone = deleted_data

    if len(dict_drone) > 0:
        return True, dict_drone, None
    else:
        return False, None, None


def upd_data_by_id(ses, data_model, uid, new_data=None):
    try:
        data = ses.query(data_model).filter_by(id=uid).one()

        if new_data is not None:
            data.drone_id = new_data["drone_id"] if "drone_id" in new_data else data.drone_id
            data.drone_name = new_data["drone_name"] if "drone_name" in new_data else data.drone_name

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
        return False, None, "drone not found"

    dict_data = data.to_dict()

    if len(dict_data) > 0:
        return True, dict_data, None
    else:
        return False, None, None
