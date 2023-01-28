from sqlalchemy import JSON
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc
from db import Traces, Components, Datasets
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db import delete_trace


session_maker = sessionmaker(bind=create_engine('sqlite:///db/models.db'))

# def delete_all_trace_of_component(component_id:int, session: Session) -> bool:
#     session.query(Traces).filter_by(component_id = component_id).delete()
#     session.commit()

# with session_maker() as session:
#     delete_all_trace_of_component(1, session)


with session_maker() as session:
    delete_trace(3, session)