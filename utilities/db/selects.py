from sqlalchemy import JSON
from sqlalchemy.orm import Session
from .models import Traces, Components


def name_exists(name: str, session: Session) -> bool:
    result = session.query(Components).filter_by(name=name).first()
    return result is not None


def components_count(session: Session):
    num_rows = session.query(Components).count()
    return num_rows