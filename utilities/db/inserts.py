from sqlalchemy import JSON
from sqlalchemy.orm import Session
from .models import Traces, Components, Datasets

def add_trace(component_id: int, args: JSON, session: Session) -> None:
    trace = Traces(component_id=component_id, args=args)
    session.add(trace)
    session.commit()
    

def add_component(name: str, session: Session) -> None:
    component = Components(name=name)
    session.add(component)
    session.commit()

def add_dataset(name: str, data: JSON, session: Session) -> None:
    dataset = Datasets(name=name, data=data)
    session.add(dataset),
    session.commit()