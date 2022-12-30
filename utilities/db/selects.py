from sqlalchemy import JSON, exists
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc
from .models import Traces, Components, Datasets


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

# Traces
def trace_name_exists(component_id: int, trace_name: str, session: Session) -> bool:
    result = session.query(exists().where(Traces.component_id == component_id).where(Traces.trace_name == trace_name)).scalar()
    return result

def traces_count(session: Session):
    num_rows = session.query(Traces).count()
    return num_rows

def get_all_traces(component_id, session: Session):
    return session.query(Traces).filter(Traces.component_id == component_id).order_by(desc(Traces.created_at)).all()