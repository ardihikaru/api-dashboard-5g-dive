from app import Base
from sqlalchemy import text, Column, Integer, String, TIMESTAMP


class NodeModel(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id = Column(String(3))
    node_name = Column(String(50))
    identifier = Column(String(150))
    create_time = Column(TIMESTAMP, server_default=text('(now())'))

    def to_dict(self):
        user_info = {
            'id': self.id,
            'node_id': self.node_id,
            'node_name': self.node_name,
            'create_time': self.create_time
        }
        return user_info
