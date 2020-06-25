from app import Base
from sqlalchemy import text, Column, Integer, TIMESTAMP, Float


class GpuRamModel(Base):
    __tablename__ = 'gpu_ram'
    id = Column(Integer, primary_key=True, autoincrement=True)
    util_gb = Column(Float(5))
    util_percent = Column(Float(5))
    timestamp = Column(TIMESTAMP, server_default=text('(now())'))

    def to_dict(self):
        user_info = {
            'id': self.id,
            'util_gb': self.util_gb,
            'util_percent': self.util_percent,
            'timestamp': self.timestamp
        }
        return user_info

    def insert(self, ses, data):
        ses.add(
            GpuRamModel(
                util_gb=data["util_gb"],
                util_percent=data["util_percent"]
            )
        )

