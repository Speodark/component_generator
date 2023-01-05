from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, JSON, ForeignKey, UniqueConstraint, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Traces(Base):
    __tablename__ = 'traces'
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id', ondelete='CASCADE'), nullable=False)
    trace_name = Column(String)
    dataset_id = Column(Integer, ForeignKey('datasets.id', ondelete='SET NULL'))
    created_at = Column(DateTime, default=datetime.utcnow)
    args = Column(JSON)
    active_columns = Column(JSON, default=None)
    __table_args__ = (UniqueConstraint('component_id', 'trace_name', name='uix_1'),)
    component = relationship("Components", back_populates="traces")
    dataset = relationship("Datasets", back_populates="traces")

class Components(Base):
    __tablename__ = 'components'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    traces = relationship("Traces", back_populates="component", cascade="all, delete-orphan")

class Datasets(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON)
    traces = relationship("Traces", back_populates="dataset")

@event.listens_for(Traces.__table__, 'after_update')
def set_active_columns_to_null(mapper, connection, target):
    if target.dataset_id is None:
        connection.execute(
            Traces.__table__.update().where(Traces.__table__.c.id == target.id).values(active_columns=None)
        )