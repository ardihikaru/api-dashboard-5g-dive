from app import app, engine, local_settings
from app.addons.utils import json_load_str, get_json_template
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
from .drone_model import DroneModel
from .drone_functions import get_all_drones, get_drone_by_drone_id, del_drone_by_drone_id, del_all_drones, \
    insert_new_data, upd_data_by_id, get_data_by_uid, del_data_by_id
import simplejson as json


class Drone(DroneModel):
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
        if "drone_id" not in json_data:
            return False, "Drone ID should not be EMPTY."

        if "drone_name" not in json_data:
            return False, "Drone Name should not be EMPTY."

        if is_input_valid:
            is_id_exist, _ = get_drone_by_drone_id(ses, Drone, json_data["drone_id"])
            if is_id_exist:
                return False, "Drone ID `%s` exist." % json_data["drone_id"]

        return True, None

    def trx_register(self, ses, json_data):
        is_valid, msg = self.__validate_register_data(ses, json_data)

        self.set_resp_status(is_valid)
        self.set_msg(msg)

        if is_valid:
            msg = "Registering a new drone device succeed."
            _, json_data = insert_new_data(ses, DroneModel, json_data)
            self.set_msg(msg)

        self.set_resp_data(json_data)

    def register(self, json_data):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_register(var, json_data))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_drones(self, ses, get_args=None):
        is_valid, drones = get_all_drones(ses, Drone, get_args)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(drones)

    def __extract_get_args(self, get_args):
        if get_args is not None:
            if "filter" in get_args:
                get_args["filter"] = json_load_str(get_args["filter"], "dict")
            if "range" in get_args:
                get_args["range"] = json_load_str(get_args["range"], "list")
            if "sort" in get_args:
                get_args["sort"] = json_load_str(get_args["sort"], "list")

        return get_args

    def get_drones(self, get_args=None):
        get_args = self.__extract_get_args(get_args)
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_drones(var, get_args=get_args))
        return get_json_template(response=self.resp_status, results=self.resp_data, message=self.msg)

    def trx_get_data_by_drone_id(self, ses, drone_id):
        is_valid, drone_data = get_drone_by_drone_id(ses, Drone, drone_id)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(drone_data)

    def get_data_by_drone_id(self, drone_id):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_data_by_drone_id(var, drone_id))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_del_data_by_drone_id(self, ses, drone_id):
        is_valid, drone_data, msg = del_drone_by_drone_id(ses, Drone, drone_id)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

        self.set_resp_data(drone_data)

    def delete_data_by_drone_id(self, drone_id):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_data_by_drone_id(var, drone_id))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_del_all_data(self, ses):
        is_valid, drone_data, msg = del_all_drones(ses, Drone)
        if drone_data is None:
            is_valid = False
            msg = "drone not found"
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting all drones success.")

        self.set_resp_data(drone_data)

    def delete_all_drones(self):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_all_data(var))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_upd_data_by_id(self, ses, uid, json_data):
        is_valid, data, msg = upd_data_by_id(ses, Drone, uid, new_data=json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Updating data success.")

        self.set_resp_data(data)

    def update_data_by_id(self, uid, json_data):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_upd_data_by_id(var, uid, json_data))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_data_by_uid(self, ses, uid):
        is_valid, drone_data = get_data_by_uid(ses, Drone, uid)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(drone_data)

    def get_data_by_id(self, uid):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_data_by_uid(var, uid))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_del_data_by_id(self, ses, uid):
        is_valid, drone_data, msg = del_data_by_id(ses, Drone, uid)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

        self.set_resp_data(drone_data)

    def delete_data_by_id(self, uid):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_data_by_id(var, uid))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
