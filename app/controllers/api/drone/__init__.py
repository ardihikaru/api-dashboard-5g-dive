from flask_restplus import Namespace, fields

api = Namespace('drones', description='User related operations')

register_drone = api.model('register_drone', {
    'drone_id': fields.String,
    'drone_name': fields.String,
})

register_drone_resp = api.model('register_drone_resp', {
    'id': fields.String,
    'drone_id': fields.String,
    'drone_name': fields.String,
})

register_drone_results = api.model('register_drone_results', {
    'response': fields.Boolean,
    'results': fields.Nested(register_drone_resp),
    'message': fields.String,
})

all_drone_data = api.model('all_drone_data', {
    'response': fields.Boolean,
    'results': fields.List(fields.Nested(register_drone_resp)),
    'message': fields.String,
    'total': fields.Integer,
})
