from app import api
from .auth.auth import api as auth_api
from .user.user import api as user_api
from .drone.drone import api as drone_api
from .node.node import api as node_api

api.add_namespace(auth_api)
api.add_namespace(user_api)
api.add_namespace(drone_api)
api.add_namespace(node_api)
