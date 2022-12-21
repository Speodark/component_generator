from sqlalchemy import JSON
from sqlalchemy.orm import Session
from .models import Traces, Components

def update_trace(trace_id: int, new_args: JSON, session: Session) -> None:
    trace = session.query(Traces).filter_by(id=trace_id).first()
    trace.args = new_args
    session.commit()


def rename_component(component_id: int, new_name: str, session: Session) -> None:
    component = session.query(Components).filter(Components.id == component_id).first()
    component.name = new_name
    session.commit()