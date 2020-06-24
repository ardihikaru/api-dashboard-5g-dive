from app import app, engine, local_settings
from app.addons.utils import json_load_str, get_json_template
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
from .frame_model import FrameModel
from ..drone.drone_model import DroneModel
from ..node.node_model import NodeModel
from .frame_functions import get_all_frames, get_frame_by_frame_id, del_frame_by_frame_id
from ..drone.drone_functions import get_drone_by_drone_id
from ..node.node_functions import get_node_by_node_id
import simplejson as json


class Frame(FrameModel):
    def __init__(self):
        self.resp_status = None
        self.resp_data = None
        self.msg = None
        self.password_hash = None

    def set_resp_status(self, status):
        self.resp_status = status

    def set_resp_data(self, json_data):
        self.resp_data = json_data

    def set_msg(self, msg):
        self.msg = msg

    def __validate_register_data(self, ses, json_data):
        is_input_valid = True
        if "frame_id" not in json_data:
            return False, "Frame ID should not be EMPTY."

        if "drone_id" not in json_data:
            return False, "Drone ID should not be EMPTY."

        if "node_id" not in json_data:
            return False, "Node ID should not be EMPTY."

        if "frame_name" not in json_data:
            return False, "Frame Name should not be EMPTY."

        if is_input_valid:
            is_fid_exist, _ = get_frame_by_frame_id(ses, Frame, json_data["frame_id"])
            if is_fid_exist:
                return False, "Frame ID `%s` exist." % json_data["frame_id"]

            is_did_exist, _ = get_drone_by_drone_id(ses, DroneModel, json_data["drone_id"])
            if not is_did_exist:
                return False, "Unable to find Drone ID `%s`." % json_data["drone_id"]

            is_nid_exist, _ = get_node_by_node_id(ses, NodeModel, json_data["node_id"])
            if not is_nid_exist:
                return False, "Unable to find Node ID `%s`." % json_data["node_id"]

        return True, None

    def trx_register(self, ses, json_data):
        is_valid, msg = self.__validate_register_data(ses, json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)

        if is_valid:
            msg = "Registering a new Frame device succeed."
            self.insert(ses, json_data)
            self.set_msg(msg)

        self.set_resp_data(json_data)

    def register(self, json_data):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_register(var, json_data))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_frames(self, ses, get_args=None):
        is_valid, frames = get_all_frames(ses, Frame)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(frames)

    def __extract_get_args(self, get_args):
        if get_args is not None:
            if "filter" in get_args:
                get_args["filter"] = json_load_str(get_args["filter"], "dict")
            if "range" in get_args:
                get_args["range"] = json_load_str(get_args["range"], "list")
            if "sort" in get_args:
                get_args["sort"] = json_load_str(get_args["sort"], "list")

        return get_args

    def get_frames(self, get_args=None):
        get_args = self.__extract_get_args(get_args)
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_frames(var, get_args=get_args))
        return get_json_template(response=self.resp_status, results=self.resp_data, message=self.msg)

    def trx_get_data_by_frame_id(self, ses, frame_id):
        is_valid, frame_data = get_frame_by_frame_id(ses, Frame, frame_id)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(frame_data)

    def get_data_by_frame_id(self, frame_id):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_data_by_frame_id(var, frame_id))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_del_data_by_frame_id(self, ses, frame_id):
        is_valid, frame_data, msg = del_frame_by_frame_id(ses, Frame, frame_id)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

        self.set_resp_data(frame_data)

    def delete_data_by_frame_id(self, frame_id):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_data_by_frame_id(var, frame_id))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
