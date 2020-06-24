from flask_restplus import Resource, abort
from flask import request
from app.addons.utils import masked_json_template
from app.models.frame.frame import Frame
from . import *


@api.route('')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class FrameRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_frame_results)
    @api.expect(register_frame)
    def post(self):
        '''Add new Frame'''
        try:
            json_data = api.payload
            resp = Frame().register(json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_list_with(all_frame_data)
    def get(self):
        '''Get Frame data'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None

            resp = Frame().get_frames(get_args)
            if resp["results"] is None:
                resp["results"] = []

            return resp
            # return masked_json_template(resp, 200, no_checking=True)
        except:
            abort(400, "Input unrecognizable.")

@api.route('/<frame_name>')  # frame_<frame_id>_<drone_id>_<node_id>
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class FrameFindRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_frame_results)
    def get(self, frame_name):
        '''Get Frame data by Frame ID'''
        try:
            resp = Frame().get_data_by_frame_name(frame_name)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(register_frame_results)
    def delete(self, frame_id):
        '''Delete Frame data by Frame ID'''
        try:
            resp = Frame().delete_data_by_frame_name(frame_name)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")
