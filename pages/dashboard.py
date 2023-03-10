from dash import html, dcc, dash_table
from pprint import pprint
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from callbacks import *
from components import *
from app import TITLE
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import components_count, get_all_components, get_all_traces, get_newest_component
from pages_components.dashboard import *
import dash

dash.register_page(
    __name__,
    title = TITLE,
    path = '/'
)

session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))


def dashboard_args():
    return dmc.Tabs(
        children=[
            dmc.TabsList(
                [
                    dmc.Tab("Data", value='Data'),
                    dmc.Tab("Traces", value='Traces'),
                    dmc.Tab("Settings", value='Settings'),
                ],
                grow=True
            ),
            dmc.TabsPanel(dashboard_data_tab(session_maker), value="Data"),
            dmc.TabsPanel(dashboard_traces_tab(session_maker), value="Traces"),
            dmc.TabsPanel([], value="Settings"),
        ],
        value='Data'
    )



def generate_figure():
    traces = []
    # Get all traces
    with session_maker() as session:
        component = get_newest_component(session)
        if component is not None:
            traces = [trace.args for trace in get_all_traces(component.id, session)]
    # Checks that all traces are valid in case of a server side database error
    working_traces = []
    for trace in traces:
        try:
            go.Figure(data=[trace])
            working_traces.append(trace)
        except Exception as e:
            print(trace['name'], "Has Invalid properties for some reason!")
    # generate the figure
    return go.Figure(
        data=working_traces
    )

def layout():
    return html.Div(
        className='dashboard',
        children=[
            html.Div(
                className='dashboard__args',
                children=dashboard_args()
            ),
            # The component figure
            dcc.Graph(
                className='dashboard__fig fill-parent-div',
                id='main-figure',
                figure=generate_figure()
            ),
            dashboard_components_section(session_maker),
        ]
    )
