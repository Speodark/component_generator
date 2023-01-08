from sqlalchemy import JSON, exists
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc
from .models import Traces, Components, Datasets
from typing import List

# COMPONENTS
def component_name_exists(name: str, session: Session) -> bool:
    result = session.query(Components).filter_by(name=name).first()
    return result is not None


def components_count(session: Session):
    num_rows = session.query(Components).count()
    return num_rows


def get_all_components(session: Session):
    return session.query(Components).order_by(desc(Components.created_at)).all()


def get_newest_component(session: Session):
    return session.query(Components).order_by(Components.created_at.desc()).first()


# DATASETS
def dataset_name_exists(name: str, session: Session) -> bool:
    result = session.query(Datasets).filter_by(name=name).first()
    return result is not None


def datasets_count(session: Session):
    num_rows = session.query(Datasets).count()
    return num_rows


def get_all_datasets(session: Session):
    return session.query(Datasets).order_by(desc(Datasets.created_at)).all()


def get_dataset(dataset_id: int, session: Session):
    return session.query(Datasets).filter_by(id=dataset_id).first()


def dataset_is_connected_to_traces(dataset_id: int, session: Session) -> bool:
    # query for traces with the given dataset ID
    traces = session.query(Traces).filter_by(dataset_id=dataset_id).all()

    # return True if there are any traces with the given dataset ID, False otherwise
    return bool(traces)


# Traces
def trace_name_exists(component_id: int, trace_name: str, session: Session) -> bool:
    result = session.query(exists().where(Traces.component_id == component_id).where(Traces.trace_name == trace_name)).scalar()
    return result

def traces_count(session: Session):
    num_rows = session.query(Traces).count()
    return num_rows

def component_traces_count(component_id: int, session: Session):
    num_rows = session.query(Traces).filter(Traces.component_id == component_id).count()
    return num_rows

def get_all_traces(component_id: int, session: Session):
    return session.query(Traces).filter(Traces.component_id == component_id).order_by(desc(Traces.created_at)).all()

def get_trace_name(trace_id: int, session: Session):
    return session.query(Traces).filter(Traces.id == trace_id).first().trace_name

def get_trace(trace_id: int, session: Session):
    return session.query(Traces).filter(Traces.id == trace_id).first()

def get_traces_by_dataset_id(dataset_id: int, session: Session) -> List[Traces]:
    # query for traces with the given dataset ID
    traces = session.query(Traces).filter_by(dataset_id=dataset_id).all()

    # return the list of traces
    return traces