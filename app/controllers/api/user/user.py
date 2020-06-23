from flask_restplus import Resource, abort
from flask import request
from app.addons.database_blacklist.blacklist_helpers import is_token_valid
from app.addons.utils import masked_json_template
from app.models.user.user import User
from . import *

# @api.route('/<username>')
# # @api.hide
# @api.response(404, 'Json Input should be provided.')
# @api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
# class UserIDRoute(Resource):
#     # @api.marshal_with(user_results)
#     def get(self, username):
#         '''Get data users (filterable)'''
#         is_valid, code, msg   = is_token_valid(request.headers.get('Authorization'))
#         if is_valid:
#             try:
#                 encoded_token = request.headers.get('Authorization').replace('Bearer ', '')
#                 resp = User().get_user(encoded_token, username)
#                 return masked_json_template(resp, 200)
#             except:
#                 abort(400, "JSON Input unrecognizable.")
#         else:
#             abort(code, msg)
#
#     # @api.marshal_with(user_results)
#     def delete(self, username):
#         '''Get data users (filterable)'''
#         is_valid, code, msg   = is_token_valid(request.headers.get('Authorization'))
#         if is_valid:
#             try:
#                 encoded_token = request.headers.get('Authorization').replace('Bearer ', '')
#                 resp = User().deleting_user(encoded_token, username)
#                 return masked_json_template(resp, 403)
#             except:
#                 abort(400, "JSON Input unrecognizable.")
#         else:
#             abort(code, msg)


@api.route('')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class UserRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_results)
    @api.expect(register_data)
    def post(self):
        '''Add new user'''
        try:
            json_data = api.payload
            resp = User().register(json_data)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    # @api.marshal_with(all_user_data)
    @api.marshal_list_with(all_user_data)
    # @api.marshal_with(all_user_data, as_list=True)
    def get(self):
        '''Get user data'''
        try:
            try:
                get_args = {
                    "filter": request.args.get('filter', default="", type=str),
                    "range": request.args.get('range', default="", type=str),
                    "sort": request.args.get('sort', default="", type=str)
                }
            except:
                get_args = None

            resp = User().get_users(get_args)
            print(" --- resp:", resp)
            # return resp
            return masked_json_template(resp, 200, no_checking=True)
        except:
            abort(400, "Input unrecognizable.")

@api.route('/<username>')
# @api.hide
@api.response(404, 'Json Input should be provided.')
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class UserFindRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(register_data_resp)
    def get(self, username):
        '''Delete user data by username'''
        try:
            resp = User().get_data_by_username(username)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")

    @api.doc(security=None)
    @api.marshal_with(register_results)
    def delete(self, username):
        '''Delete user data by username'''
        try:
            resp = User().delete_data_by_username(username)
            return masked_json_template(resp, 200)
        except:
            abort(400, "Input unrecognizable.")
