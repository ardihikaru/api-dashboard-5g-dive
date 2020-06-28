from flask_restplus import Namespace, fields

api = Namespace('nodes', description='User related operations')

register_node = api.model('register_node', {
    'node_id': fields.String,
    'node_name': fields.String,
})

register_node_resp = api.model('register_node_resp', {
    'id': fields.String,
    'node_id': fields.String,
    'node_name': fields.String,
})

register_node_results = api.model('register_node_results', {
    'response': fields.Boolean,
    'results': fields.Nested(register_node_resp),
    'message': fields.String,
})

all_node_data = api.model('all_node_data', {
    'response': fields.Boolean,
    'results': fields.List(fields.Nested(register_node_resp)),
    'message': fields.String,
    'total': fields.Integer,
})

delete_node_results = api.model('delete_node_results', {
    'response': fields.Boolean,
    'message': fields.String,
})

editable_data = api.model('editable_data', {
    'node_id': fields.String,
    'node_name': fields.String,
})