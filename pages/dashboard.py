from dash import html, dcc, dash_table
from pprint import pprint
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from callbacks.callbacks import *
from components import *
from app import TITLE
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import components_count, get_all_components, get_all_traces, get_newest_component
from pages_components.dashboard import *

dash.register_page(
    __name__,
    title = TITLE,
    path = '/'
)

session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))




def dashboard_args():
    return dmc.Tabs(
        grow=True,
        children=[
            dashboard_data_tab(session_maker),
            dashboard_traces_tab(session_maker),
            dmc.Tab(
                id='args-tab',
                label="args", 
                children=[]
            ),
        ]
    )



def generate_figure():
    traces = []
    with session_maker() as session:
        component_id = get_newest_component(session).id
        traces = [trace.args for trace in get_all_traces(component_id, session)]
    return go.Figure(
        data=traces
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
