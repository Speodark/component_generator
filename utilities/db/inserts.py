from sqlalchemy import JSON
from sqlalchemy.orm import Session
from .models import Traces, Components, Datasets

def add_trace(trace_name: str ,component_id: int, args: JSON, session: Session, dataset_id: int = None, commit = True) -> None:
    trace = Traces(component_id=component_id, trace_name=trace_name, dataset_id=dataset_id, args=args)
    session.add(trace)
    if commit:
        session.commit()
    

def add_component(name: str, session: Session, commit = True) -> None:
    component = Components(name=name)
    session.add(component)
    if commit:
        session.commit()

def add_dataset(name: str, data: JSON, session: Session, commit = True) -> None:
    dataset = Datasets(name=name, data=data)
    session.add(dataset),
    if commit:
        session.commit()