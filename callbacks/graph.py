import dash
from dash import Input, Output, State, no_update
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import get_all_traces, get_newest_component
import plotly.graph_objects as go

session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))

@dash.callback(
    Output('main-figure', 'figure'),
    Input('components-dropdown', 'value'),
    Input('added-trace-trigger','data'),
    Input('deleted_trace_trigger', 'data'),
)
def update_figure(
    component_id,
    _,
    __
):
    traces = []
    with session_maker() as session:
        traces = [trace.args for trace in get_all_traces(component_id, session)]
    return go.Figure(
        data=traces
    )