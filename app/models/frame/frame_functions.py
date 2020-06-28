from app import app, rc, local_settings
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict
from app.addons.cryptography.fernet import encrypt


def insert_new_data(ses, data_model, new_data):
    # new_data["identifier"] = encrypt(new_data["frame_name"])
    identifier_str = new_data["frame_id"] + new_data["drone_id"] + new_data["node_id"]
    new_data["identifier"] = encrypt(identifier_str)
    ses.add(data_model(
                frame_id=new_data["frame_id"],
                drone_id=new_data["drone_id"],
                node_id=new_data["node_id"],
                frame_name=new_data["frame_name"],
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


def get_all_frames(ses, frame_model, args=None):
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
        data = ses.query(frame_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except NoResultFound:
        return False, None
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict
    else:
        return False, None


def get_frame_by_frame_name(ses, frame_model, frame_name):
    try:
        data = ses.query(frame_model).filter_by(frame_name=frame_name).one()
    except NoResultFound:
        return False, None
    dict_frame = data.to_dict()

    if len(dict_frame) > 0:
        return True, dict_frame
    else:
        return False, None


def del_frame_by_frame_name(ses, frame_model, frame_name):
    try:
        data = ses.query(frame_model).filter_by(frame_name=frame_name).one()
        ses.query(frame_model).filter_by(frame_name=frame_name).delete()
    except NoResultFound:
        return False, None, "frame not found"

    dict_frame = data.to_dict()

    if len(dict_frame) > 0:
        return True, dict_frame, None
    else:
        return False, None, None

def del_all_frames(ses, data_model, args=None):
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
                    data = ses.query(data_model).filter_by(id=uid).one()
                    deleted_data.append(data.to_dict())
                    ses.query(data_model).filter_by(id=uid).delete()
                    no_filter = False
        if no_filter:
            data = ses.query(data_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except NoResultFound:
        return False, None, "Frame not found"

    if no_filter:
        dict_drone = sqlresp_to_dict(data)
    else:
        dict_drone = deleted_data

    if len(dict_drone) > 0:
        return True, dict_drone, None
    else:
        return False, None, None
    
# def del_all_frames(ses, frame_model, get_args=None):
#     try:
#         data = ses.query(frame_model).all()
#         ses.query(frame_model).delete()
#     except NoResultFound:
#         return False, None, "frame not found"
# 
#     dict_frame = sqlresp_to_dict(data)
# 
#     if len(dict_frame) > 0:
#         return True, dict_frame, None
#     else:
#         return False, None, None
