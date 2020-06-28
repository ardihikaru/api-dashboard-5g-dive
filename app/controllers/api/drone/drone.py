from flask_restplus import Resource, abort
from flask import request
from app.addons.utils import masked_json_template
from app.models.drone.drone import Drone
from . import *


@api.route('')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class DroneRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_drone_results)
    @api.expect(register_drone)
    def post(self):
        '''Add new drone'''
        try:
            json_data = api.payload
            resp = Drone().register(json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_list_with(all_drone_data)
    def get(self):
        '''Get drone data'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None

            resp = Drone().get_drones(get_args)
            if resp["results"] is None:
                resp["results"] = []

            return resp
            # return masked_json_template(resp, 200, no_checking=True)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(delete_drone_results)
    def delete(self):
        '''Delete all existing Drones'''
        try:
            resp = Drone().delete_all_drones()
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

@api.route('/<drone_id>')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class DroneFindRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_drone_results)
    def get(self, drone_id):
        '''Get drone data by drone ID'''
        try:
            resp = Drone().get_data_by_drone_id(drone_id)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(register_drone_results)
    @api.expect(editable_data)
    def put(self, drone_id):
        '''Update user data by user ID'''
        try:
            json_data = api.payload
            resp = Drone().update_data_by_id(drone_id, json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(register_drone_results)
    def delete(self, drone_id):
        '''Delete drone data by drone ID'''
        try:
            resp = Drone().delete_data_by_drone_id(drone_id)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")
