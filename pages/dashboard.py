from dash import html, dcc, dash_table
from pprint import pprint
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from callbacks.callbacks import *
from components import *


def dashboard():
    return html.Div(
        className='dashboard',
        children=[
            html.Div(
                className='dashboard__args',
                children=dmc.Tabs(
                    grow=True,
                    children=[
                        dmc.Tab(label="Data", children=[
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
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
                            )
                        ]),
                        dmc.Tab(label="Figure", children=[]),
                        dmc.Tab(id='args-tab',label="args", children=[]),
                    ]
                )
            ),
            html.Div(
                className='dashboard__graph',
                children=[
                    dcc.Dropdown(
                        options=[
                            {'label': 'Line Chart', 'value': 'line_chart'},
                            {'label': 'Bar Chart', 'value': 'bar_chart'},
                        ],
                        value='line_chart',
                        className='dashboard__graph--type',
                        id='graph-type',
                        clearable=False,
                    ),
                    dcc.Graph(
                        className='dashboard__graph--fig fill-parent-div',
                        id='graph-fig',
                    ),
                ]
            ),
            dbc.Modal(
                id='popup',
                size='xl',
            )
        ]
    )
