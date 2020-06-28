from app import app, rc, local_settings
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict
from sqlalchemy import desc
from app.addons.cryptography.fernet import encrypt


def insert_new_data(ses, data_model, new_data):
    new_data["identifier"] = encrypt(str(new_data["util_gb"]))
    ses.add(data_model(
                util_gb=new_data["util_gb"],
                util_percent=new_data["util_percent"],
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
    dict_user = data.to_dict()

    if len(dict_user) > 0:
        return True, dict_user
    else:
        return False, None


def get_all_data(ses, data_model, args=None):
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
        data = ses.query(data_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except NoResultFound:
        return False, None
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict
    else:
        return False, None


def del_all_data(ses, data_model):
    try:
        data = ses.query(data_model).all()
        ses.query(data_model).delete()
    except NoResultFound:
        return False, None, "CPU RAM data not found"

    dict_data = sqlresp_to_dict(data)

    if len(dict_data) > 0:
        return True, dict_data, None
    else:
        return False, None, None


def get_latest_data(ses, data_model):
    try:
        data = ses.query(data_model).order_by(desc(data_model.timestamp)).limit(1).first()
    except NoResultFound:
        return False, None, "CPU RAM data not found"
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict, None
    else:
        return False, None, None

