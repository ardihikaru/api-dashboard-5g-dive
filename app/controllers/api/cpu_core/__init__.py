from flask_restplus import Namespace, fields

api = Namespace('util', description='User related operations')

register_cpu_core = api.model('register_cpu_core', {
    'util_num': fields.Float,
    'util_percent': fields.Float,
})

register_cpu_core_resp = api.model('register_cpu_core_resp', {
    'id': fields.String,
    'util_num': fields.Float,
    'util_percent': fields.Float,
    'timestamp': fields.String,
})

register_cpu_core_results = api.model('register_cpu_core_results', {
    'response': fields.Boolean,
    'results': fields.Nested(register_cpu_core_resp),
    'message': fields.String,
})

all_cpu_core_data = api.model('all_cpu_core_data', {
    'response': fields.Boolean,
    'results': fields.List(fields.Nested(register_cpu_core_resp)),
    'message': fields.String,
    'total': fields.Integer,
})

delete_cpu_core_results = api.model('delete_cpu_core_results', {
    'response': fields.Boolean,
    'message': fields.String,
})
