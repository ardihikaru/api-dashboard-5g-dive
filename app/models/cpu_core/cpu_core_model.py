from app import Base
from sqlalchemy import text, Column, Integer, TIMESTAMP, Float, String


class CpuCoreModel(Base):
    __tablename__ = 'cpu_core'
    id = Column(Integer, primary_key=True, autoincrement=True)
    util_num = Column(Float(5))
    util_percent = Column(Float(5))
    identifier = Column(String(150))
    timestamp = Column(TIMESTAMP, server_default=text('(now())'))

    def to_dict(self):
        user_info = {
            'id': self.id,
            'util_num': self.util_num,
            'util_percent': self.util_percent,
            'timestamp': self.timestamp
        }
        return user_info
