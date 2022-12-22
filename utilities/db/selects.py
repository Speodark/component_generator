from sqlalchemy import JSON
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


# DATASETS
def dataset_name_exists(name: str, session: Session) -> bool:
    result = session.query(Datasets).filter_by(name=name).first()
    return result is not None


def datasets_count(session: Session):
    num_rows = session.query(Datasets).count()
    return num_rows


def get_all_datasets(session: Session):
    return session.query(Datasets).order_by(desc(Datasets.created_at)).all()