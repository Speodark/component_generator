from sqlalchemy import JSON
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc
from .models import Traces, Components


def delete_component_by_id(component_id: int, session: Session) -> bool:
    component = session.query(Components).filter_by(id=component_id).first()
    if component:
        session.delete(component)
        session.commit()