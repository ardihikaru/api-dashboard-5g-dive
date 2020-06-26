from app import app, rc, local_settings
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict
from sqlalchemy import desc


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
        return False, None, "GPU RAM data not found"

    dict_data = sqlresp_to_dict(data)

    if len(dict_data) > 0:
        return True, dict_data, None
    else:
        return False, None, None


def get_latest_data(ses, data_model):
    try:
        data = ses.query(data_model).order_by(desc(data_model.timestamp)).limit(1).first()
    except NoResultFound:
        return False, None, "GPU RAM data not found"
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict, None
    else:
        return False, None, None

