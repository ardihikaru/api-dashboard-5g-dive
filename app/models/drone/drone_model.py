from app import Base
from sqlalchemy import text, Column, Integer, String, TIMESTAMP


class DroneModel(Base):
    __tablename__ = 'drones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    drone_id = Column(String(3))
    drone_name = Column(String(50))
    create_time = Column(TIMESTAMP, server_default=text('(now())'))

    def to_dict(self):
        user_info = {
            'id': self.id,
            'drone_id': self.drone_id,
            'drone_name': self.drone_name,
            'create_time': self.create_time
        }
        return user_info

    def insert(self, ses, data):
        ses.add(
            DroneModel(
                drone_id=data["drone_id"],
                drone_name=data["drone_name"]
            )
        )

