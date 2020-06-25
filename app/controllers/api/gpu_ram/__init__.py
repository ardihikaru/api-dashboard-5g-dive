from flask_restplus import Namespace, fields

api = Namespace('util', description='User related operations')

register_gpu_ram = api.model('register_gpu_ram', {
    'util_gb': fields.Float,
    'util_percent': fields.Float,
})

register_gpu_ram_resp = api.model('register_gpu_ram_resp', {
    'id': fields.String,
    'util_gb': fields.Float,
    'util_percent': fields.Float,
    'timestamp': fields.String,
})

register_gpu_ram_results = api.model('register_gpu_ram_results', {
    'response': fields.Boolean,
    'results': fields.Nested(register_gpu_ram_resp),
    'message': fields.String,
})

all_gpu_ram_data = api.model('all_gpu_ram_data', {
    'response': fields.Boolean,
    'results': fields.List(fields.Nested(register_gpu_ram_resp)),
    'message': fields.String,
    'total': fields.Integer,
})

delete_gpu_ram_results = api.model('delete_gpu_ram_results', {
    'response': fields.Boolean,
    'message': fields.String,
})
