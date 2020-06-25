from app import api
from .auth.auth import api as auth_api
from .user.user import api as user_api
from .drone.drone import api as drone_api
from .node.node import api as node_api
from .frame.frame import api as frame_api
from .cpu_ram.cpu_ram import api as cpu_ram_api
from .cpu_core.cpu_core import api as cpu_core_api
from .gpu_ram.gpu_ram import api as gpu_core_api

api.add_namespace(auth_api)
api.add_namespace(user_api)
api.add_namespace(drone_api)
api.add_namespace(node_api)
api.add_namespace(frame_api)
api.add_namespace(cpu_ram_api)
api.add_namespace(cpu_core_api)
api.add_namespace(gpu_core_api)
