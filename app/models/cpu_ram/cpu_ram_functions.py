from app import app, rc
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict
from sqlalchemy import desc


def get_all_data(ses, data_model):
    try:
        data = ses.query(data_model).all()
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

