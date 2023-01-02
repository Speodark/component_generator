from sqlalchemy import JSON
from sqlalchemy.orm import Session
from .models import Traces, Components, Datasets

# Traces
def update_trace(trace_id: int, new_args: JSON, session: Session) -> None:
    trace = session.query(Traces).filter_by(id=trace_id).first()
    trace.args = new_args
    session.commit()


def update_trace_active_columns(trace_id: int, active_columns: JSON, session: Session) -> None:
    trace = session.query(Traces).filter_by(id=trace_id).first()
    trace.active_columns = active_columns
    session.commit()


def update_trace_name(trace_id: int, trace_name: str, session: Session) -> None:
    trace = session.query(Traces).filter_by(id=trace_id).first()
    trace.trace_name = trace_name
    session.commit()


def update_trace_dataset(trace_id: int, dataset_id: int, session: Session) -> None:
    trace = session.query(Traces).filter_by(id=trace_id).first()
    trace.dataset_id = dataset_id
    session.commit()

# Components
def rename_component(component_id: int, new_name: str, session: Session) -> None:
    component = session.query(Components).filter(Components.id == component_id).first()
    component.name = new_name
    session.commit()

# Datasets
def rename_dataset(dataset_id: int, new_name: str, session: Session) -> None:
    dataset = session.query(Datasets).filter(Datasets.id == dataset_id).first()
    dataset.name = new_name
    session.commit()


