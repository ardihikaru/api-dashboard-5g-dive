from flask_restplus import Resource, abort
from flask import request
from app.addons.utils import masked_json_template
from app.models.cpu_core.cpu_core import CpuCore
from . import *


@api.route('/cpu/core')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class CpuCoreRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_cpu_core_results)
    @api.expect(register_cpu_core)
    def post(self):
        '''Add new cpu_core'''
        try:
            json_data = api.payload
            resp = CpuCore().register(json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_list_with(all_cpu_core_data)
    def get(self):
        '''Get cpu_core data'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None

            resp = CpuCore().get_data(get_args)
            if resp["results"] is None:
                resp["results"] = []

            return resp
            # return masked_json_template(resp, 200, no_checking=True)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(delete_cpu_core_results)
    def delete(self):
        '''Delete all existing cpu_cores'''
        try:
            resp = CpuCore().delete_all_data()
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

@api.route('/cpu/core/latest')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class CpuCoreFindRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_cpu_core_results)
    def get(self):
        '''Get Latest data'''
        try:
            resp = CpuCore().get_latest()
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")
