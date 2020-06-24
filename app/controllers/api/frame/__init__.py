from flask_restplus import Namespace, fields

api = Namespace('frames', description='User related operations')

register_frame = api.model('register_frame', {
    'frame_id': fields.String,
    'drone_id': fields.String,
    'node_id': fields.String,
    'frame_name': fields.String,
})

register_frame_resp = api.model('register_frame_resp', {
    'id': fields.String,
    'frame_id': fields.String,
    'drone_id': fields.String,
    'node_id': fields.String,
    'frame_name': fields.String,
})

register_frame_results = api.model('register_frame_results', {
    'response': fields.Boolean,
    'results': fields.Nested(register_frame_resp),
    'message': fields.String,
})

all_frame_data = api.model('all_frame_data', {
    'response': fields.Boolean,
    'results': fields.List(fields.Nested(register_frame_resp)),
    'message': fields.String,
    'total': fields.Integer,
})

delete_frame_results = api.model('delete_frame_results', {
    'response': fields.Boolean,
    'message': fields.String,
})
