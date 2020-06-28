from flask_restplus import Resource, abort
from flask import request
from app.addons.utils import masked_json_template
from app.models.node.node import Node
from . import *


@api.route('')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class NodeRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_node_results)
    @api.expect(register_node)
    def post(self):
        '''Add new node'''
        try:
            json_data = api.payload
            resp = Node().register(json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_list_with(all_node_data)
    def get(self):
        '''Get Node data'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None

            resp = Node().get_nodes(get_args)
            if resp["results"] is None:
                resp["results"] = []

            return masked_json_template(resp, 200, no_checking=True)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(delete_node_results)
    def delete(self):
        '''Delete all existing Nodes'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None
            resp = Node().delete_all_nodes(get_args)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

@api.route('/node_id/<node_id>')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class NodeFindRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_node_results)
    def get(self, node_id):
        '''Get Node data by Node ID'''
        try:
            resp = Node().get_data_by_node_id(node_id)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(register_node_results)
    def delete(self, node_id):
        '''Delete Node data by Node ID'''
        try:
            resp = Node().delete_data_by_node_id(node_id)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")


@api.route('/<uid>')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class DroneIDFindRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_node_results)
    def get(self, uid):
        '''Get data by ID'''
        try:
            resp = Node().get_data_by_id(uid)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(register_node_results)
    @api.expect(editable_data)
    def put(self, uid):
        '''Update data by ID'''
        try:
            json_data = api.payload
            resp = Node().update_data_by_id(uid, json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(register_node_results)
    def delete(self, uid):
        '''Delete data by ID'''
        try:
            resp = Node().delete_data_by_id(uid)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")
