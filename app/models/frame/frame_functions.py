from app import app, rc
from sqlalchemy.orm.exc import NoResultFound
from app.addons.utils import sqlresp_to_dict


def get_all_frames(ses, frame_model):
    try:
        data = ses.query(frame_model).all()
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
