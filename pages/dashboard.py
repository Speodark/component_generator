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
from utilities.db import components_count

dash.register_page(
    __name__,
    title = TITLE,
    path = '/'
)

session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))

def dashboard_data_tab():
    return dmc.Tab(
        label="Data", 
        children=html.Div(
            className='center_items_vertical',
            children=[
                dcc.Upload(
                    id='upload_file',
                    children=html.Div(
                        children=[
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]
                    ),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                ),
                html.Div(
                    className='dashboard__data--filename',
                    id='current-data-file-name',
                    children='Upload a File'
                ),
                html.Button(
                    id='show-data-table-btn',
                    className='dashboard__load-popup--btn',
                    children='Show Table',
                    disabled=True
                )
            ]
        )
    )


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


def dashboard_components_section():
    is_there_components = False
    with session_maker() as session:
        num_of_components = components_count(session)
        if num_of_components > 0: 
            is_there_components = True
    print(is_there_components)
    return html.Div(
        className='dashboard__components',
        children=[
            dcc.Dropdown(
                options=[
                    {'label': 'Line Chart', 'value': 'line_chart'},
                    {'label': 'Bar Chart', 'value': 'bar_chart'},
                ],
                value='line_chart',
                className='dashboard__components--type',
                id='graph-type',
                clearable=False,
            ),
            dcc.Graph(
                className='dashboard__components--fig fill-parent-div',
                id='graph-fig',
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
            dashboard_components_section(),
            dbc.Modal(
                id='popup',
                size='xl',
                children=[
                    html.Div(
                        id='popup-file-data',
                        className='dashboard__load-popup'
                    ),
                    html.Button(
                        id='load-data-btn',
                        className='dashboard__load-popup--btn',
                        children='Load data'
                    )
                ],
                
            ),
            dbc.Modal(
                id='show-table-popup',
                size='xl',
                children=[
                    html.Div(
                        id='show-table-popup-children',
                        className='dashboard__show-table-popup'
                    ),
                    html.Button(
                        id='close-show-table-popup',
                        className='btn__red',
                        children='Close'
                    )
                ],
                
            ),
            dcc.Store(id='uploaded_data'),
            dcc.Store(id='uploaded_data_name'),
            dcc.Store(id='current_data'),
            dcc.Store(id='current_data_name'),
        ]
    )
