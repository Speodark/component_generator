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
    
    hide_elements_classname = ''
    add_component_btn_class = 'dashboard__components--add-component-btn'
    components_dropdown_options = []
    if not is_there_components:
        hide_elements_classname = 'hide'
        add_component_btn_class = 'dashboard__components--add-component-btn__while-none'
    else:
        with session_maker() as session:
            components_list = get_all_components(session)
            first_components_dropdown_option = components_list[0].id
            components_dropdown_options = [
                {'label': c.name, 'value': c.id} 
                for c in components_list
            ]
    return html.Div(
        className='dashboard__components',
        children=[
            # The Components dropdown
            dcc.Dropdown(
                options=components_dropdown_options,
                value=first_components_dropdown_option,
                className='dashboard__components--type ' + hide_elements_classname,
                id='components-dropdown',
                clearable=False,
            ),
            # Add component button
            html.Button(
                id='add-component',
                className='btn__blue center_items_vertical ' + add_component_btn_class,
                children='Add'
            ),
            # Delete component button
            html.Button(
                id='open-delete-component-popup',
                className='btn__red center_items_vertical ' + hide_elements_classname,
                children='Delete'
            ),
            # rename component button
            html.Button(
                id='rename-component',
                className='btn__green center_items_vertical ' + hide_elements_classname,
                children='Rename'
            ),
            # rename component button
            html.Button(
                id='export-component',
                className='btn__grey center_items_vertical ' + hide_elements_classname,
                children='Export'
            ),
            # The component figure
            dcc.Graph(
                className='dashboard__components--fig fill-parent-div',
                id='graph-fig',
            ),
            # The add component popup
            dbc.Modal(
                id='add-component-popup',
                size='lg',
                centered=True,
                children=html.Div(
                    className='dashboard__add-component',
                    children=[
                        # The popup title
                        html.Span(
                            className='dashboard__add-component--title',
                            children='Component Name'
                        ),
                        # The input for the component name
                        dcc.Input(
                            id='add-component-input',
                            className='dashboard__add-component--input',
                            type="text",
                            value='',
                            autoComplete='off'
                        ),
                        # If while trying to create a component there's an error this will show the error
                        html.Span(
                            id='add-component-not-available',
                            className='dashboard__add-component--warning hide',
                            children='This Name is not available. Please choose a name with 3 characters or more and is not taken'
                        ),
                        # Create the component
                        html.Button(
                            id='add-component-create-btn',
                            className='btn__blue dashboard__add-component--create-btn',
                            children='Create'
                        ),
                        # Cancel the component creation
                        html.Button(
                            id='add-component-cancel-btn',
                            className='btn__red dashboard__add-component--cancel-btn',
                            children='Cancel'
                        )
                    ]
                ),
            ),
            # The confirm delete component popup
            dbc.Modal(
                id='delete-component-popup',
                size='sm',
                centered=True,
                children=html.Div(
                    className='dashboard__delete-popup',
                    children=[
                        html.Span(
                            className='dashboard__delete-popup--title',
                            children='Are you sure you want to delete the component?'
                        ),
                        html.Span(
                            className='dashboard__delete-popup--warning',
                            children="You won't be able to retrieve the component information!"
                        ),
                        # Delete the component
                        html.Button(
                            id='delete-component-btn',
                            className='btn__red dashboard__delete-popup--delete',
                            children='Delete'
                        ),
                        # Cancel
                        html.Button(
                            id='cancel-component-delete-btn',
                            className='btn__blue dashboard__delete-popup--cancel',
                            children='Cancel'
                        ),
                    ]
                ),
            ),
            # rename component popup
            dbc.Modal(
                id='rename-component-popup',
                size='sm',
                centered=True,
                children=html.Div(
                    className='dashboard__renname-popup',
                    children=[]
                ),
            )
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
                centered=True,
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
                centered=True,
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
