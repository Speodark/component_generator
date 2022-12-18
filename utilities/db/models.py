from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Traces(Base):
    __tablename__ = 'traces'
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    args = Column(JSON)
    component = relationship("Components", back_populates="traces")


class Components(Base):
    __tablename__ = 'components'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    traces = relationship("Traces", back_populates="component")
