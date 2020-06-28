from app import Base
from sqlalchemy import text, Column, Integer, String, TIMESTAMP


class FrameModel(Base):
    __tablename__ = 'frames'
    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(String(3))
    drone_id = Column(String(3))
    node_id = Column(String(3))
    frame_name = Column(String(50))
    identifier = Column(String(150))
    create_time = Column(TIMESTAMP, server_default=text('(now())'))

    def to_dict(self):
        user_info = {
            'id': self.id,
            'frame_id': self.frame_id,
            'drone_id': self.drone_id,
            'node_id': self.node_id,
            'frame_name': self.frame_name,
            'create_time': self.create_time
        }
        return user_info
