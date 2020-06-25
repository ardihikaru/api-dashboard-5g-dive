from flask_restplus import Resource, abort
from flask import request
from app.addons.utils import masked_json_template
from app.models.cpu_ram.cpu_ram import CpuRam
from . import *


@api.route('/cpu/ram')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class CpuRamRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_cpu_ram_results)
    @api.expect(register_cpu_ram)
    def post(self):
        '''Add new cpu_ram'''
        try:
            json_data = api.payload
            resp = CpuRam().register(json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_list_with(all_cpu_ram_data)
    def get(self):
        '''Get cpu_ram data'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None

            resp = CpuRam().get_data(get_args)
            if resp["results"] is None:
                resp["results"] = []

            return resp
            # return masked_json_template(resp, 200, no_checking=True)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(delete_cpu_ram_results)
    def delete(self):
        '''Delete all existing cpu_rams'''
        try:
            resp = CpuRam().delete_all_data()
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")
