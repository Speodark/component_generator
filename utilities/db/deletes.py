from sqlalchemy import JSON
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc
from .models import Traces, Components, Datasets


def delete_component_by_id(component_id: int, session: Session) -> bool:
    component = session.query(Components).filter_by(id=component_id).first()
    if component:
        session.delete(component)
        session.commit()


def delete_dataset(dataset_id: int, session: Session) -> bool:
    dataset = session.query(Datasets).filter_by(id=dataset_id).first()
    if dataset:
        session.delete(dataset)
        session.commit()


def delete_trace(trace_id: int, session: Session) -> bool:
    trace = session.query(Traces).filter_by(id=trace_id).first()
    if trace:
        session.delete(trace)
        session.commit()