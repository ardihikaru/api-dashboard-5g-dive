from app import app, engine, local_settings
from app.addons.utils import json_load_str, get_json_template
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
from .node_model import NodeModel
from .node_functions import get_all_nodes, get_node_by_node_id, del_node_by_node_id, del_all_nodes
import simplejson as json


class Node(NodeModel):
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
        if "node_id" not in json_data:
            return False, "Node ID should not be EMPTY."

        if "node_name" not in json_data:
            return False, "Node Name should not be EMPTY."

        if is_input_valid:
            is_id_exist, _ = get_node_by_node_id(ses, Node, json_data["node_id"])
            if is_id_exist:
                return False, "Node ID `%s` exist." % json_data["node_id"]

        return True, None

    def trx_register(self, ses, json_data):
        is_valid, msg = self.__validate_register_data(ses, json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)

        if is_valid:
            msg = "Registering a new Node device succeed."
            self.insert(ses, json_data)
            self.set_msg(msg)

        self.set_resp_data(json_data)

    def register(self, json_data):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_register(var, json_data))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_nodes(self, ses, get_args=None):
        is_valid, nodes = get_all_nodes(ses, Node, get_args)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(nodes)

    def __extract_get_args(self, get_args):
        if get_args is not None:
            if "filter" in get_args:
                get_args["filter"] = json_load_str(get_args["filter"], "dict")
            if "range" in get_args:
                get_args["range"] = json_load_str(get_args["range"], "list")
            if "sort" in get_args:
                get_args["sort"] = json_load_str(get_args["sort"], "list")

        return get_args

    def get_nodes(self, get_args=None):
        get_args = self.__extract_get_args(get_args)
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_nodes(var, get_args=get_args))
        return get_json_template(response=self.resp_status, results=self.resp_data, message=self.msg)

    def trx_get_data_by_node_id(self, ses, node_id):
        is_valid, node_data = get_node_by_node_id(ses, Node, node_id)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(node_data)

    def get_data_by_node_id(self, node_id):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_get_data_by_node_id(var, node_id))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_del_data_by_node_id(self, ses, node_id):
        is_valid, node_data, msg = del_node_by_node_id(ses, Node, node_id)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

        self.set_resp_data(node_data)

    def delete_data_by_node_id(self, node_id):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_data_by_node_id(var, node_id))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_del_all_data(self, ses):
        is_valid, frame_data, msg = del_all_nodes(ses, Node)
        if frame_data is None:
            is_valid = False
            msg = "node not found"
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting all nodes success.")

        self.set_resp_data(frame_data)

    def delete_all_nodes(self):
        run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_all_data(var))
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
