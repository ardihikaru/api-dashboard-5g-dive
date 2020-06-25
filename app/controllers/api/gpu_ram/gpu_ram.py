from flask_restplus import Resource, abort
from flask import request
from app.addons.utils import masked_json_template
from app.models.gpu_ram.gpu_ram import GpuRam
from . import *


@api.route('/gpu/ram')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class GpuRamRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_gpu_ram_results)
    @api.expect(register_gpu_ram)
    def post(self):
        '''Add new gpu_ram'''
        try:
            json_data = api.payload
            resp = GpuRam().register(json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_list_with(all_gpu_ram_data)
    def get(self):
        '''Get gpu_ram data'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None

            resp = GpuRam().get_data(get_args)
            if resp["results"] is None:
                resp["results"] = []

            return resp
            # return masked_json_template(resp, 200, no_checking=True)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(delete_gpu_ram_results)
    def delete(self):
        '''Delete all existing gpu_rams'''
        try:
            resp = GpuRam().delete_all_data()
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

@api.route('/gpu/ram/latest')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class GpuRamFindRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_gpu_ram_results)
    def get(self):
        '''Get Latest data'''
        try:
            resp = GpuRam().get_latest()
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")
