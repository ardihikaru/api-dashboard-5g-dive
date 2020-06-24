from app import app, rc
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict


def get_all_drones(ses, drone_model):
    try:
        data = ses.query(drone_model).all()
    except NoResultFound:
        return False, None
    data_dict = sqlresp_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict
    else:
        return False, None


def get_drone_by_drone_id(ses, drone_model, drone_id, show_passwd=False):
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
