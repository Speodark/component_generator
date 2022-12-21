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
from utilities.db import components_count, get_all_components
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
            dashboard_data_tab(),
            dmc.Tab(
                label="Graph Traces", 
                children=html.Div(
                    className='center_items_vertical',
                    children=[
                        html.Div(
                            className='dashboard__traces',
                            children=[]
                        ),
                        html.Button(
                            id='add-trace',
                            className='btn__blue',
                            children='Add Trace'
                        )
                    ]
                )
            ),
            dmc.Tab(
                id='args-tab',
                label="args", 
                children=[]
            ),
        ]
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
                id='graph-fig',
                figure=go.Figure([go.Bar(), go.Scatter()])
            ),
            dashboard_components_section(session_maker),
        ]
    )
