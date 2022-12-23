from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from utilities.db import datasets_count, get_all_datasets
from components import dataset_card


def add_dataset_popup():
    return dbc.Modal(
        id='add-dataset-popup',
        size='xl',
        centered=True,
        children=html.Div(
            className='dashboard__data--load-popup',
            children=[
                html.Div(
                    id='popup-file-data',
                    className='dashboard__data--load-popup__data'
                ),
                html.Div(
                    className='dashboard__data--load-popup__input-container',
                    children=[
                        html.Span(
                            className='dashboard__data--load-popup__input-title',
                            children='Dataset Name - '
                        ),
                        # The input for the component name
                        dcc.Input(
                            id='load-dataset-name',
                            className='dashboard__data--load-popup__input',
                            type="text",
                            value='',
                            autoComplete='off'
                        ),
                    ]
                ),
                # If while trying to create a component there's an error this will show the error
                html.Span(
                    id='load-dataset-warning',
                    className='dashboard__data--load-popup__warning hide',
                    children=''
                ),
                # Create the component
                html.Button(
                    id='load-data-btn',
                    className='btn__green dashboard__data--load-popup__load',
                    children='Load'
                ),
                # Cancel the component creation
                html.Button(
                    id='cancel-load-data-btn',
                    className='btn__red dashboard__data--load-popup__cancel',
                    children='Cancel'
                )
            ]
        )
    )


def delete_dataset_popup():
    return dbc.Modal(
        id='delete-dataset-popup',
        size='sm',
        centered=True,
        children=html.Div(
            className='dashboard__delete-popup',
            children=[
                dcc.Store(id='dataset_id_to_delete'),
                html.Span(
                    className='dashboard__delete-popup--title',
                    children='Are you sure you want to delete the dataset?'
                ),
                html.Span(
                    className='dashboard__delete-popup--warning',
                    children="You won't be able to retrieve the dataset information!"
                ),
                # Delete the component
                html.Button(
                    id='delete-dataset-btn',
                    className='btn__red dashboard__delete-popup--delete',
                    children='Delete'
                ),
                # Cancel
                html.Button(
                    id='cancel-dataset-delete-btn',
                    className='btn__blue dashboard__delete-popup--cancel',
                    children='Cancel'
                ),
            ]
        ),
    )


def rename_dataset_popup():
    return dbc.Modal(
        id='rename-dataset-popup',
        size='lg',
        centered=True,
        children=html.Div(
            className='dashboard__add-component',
            children=[
                dcc.Store(id='dataset_id_to_rename'),
                # The popup title
                html.Span(
                    className='dashboard__add-component--title',
                    children='New Name'
                ),
                # The input for the component name
                dcc.Input(
                    id='rename-dataset-input',
                    className='dashboard__add-component--input',
                    type="text",
                    value='',
                    autoComplete='off'
                ),
                # If while trying to create a component there's an error this will show the error
                html.Span(
                    id='rename-dataset-warning',
                    className='dashboard__add-component--warning hide',
                    children=''
                ),
                # Create the component
                html.Button(
                    id='rename-dataset-confirm-btn',
                    className='btn__green dashboard__add-component--create-btn',
                    children='Rename'
                ),
                # Cancel the component creation
                html.Button(
                    id='rename-dataset-cancel-btn',
                    className='btn__red dashboard__add-component--cancel-btn',
                    children='Cancel'
                )
            ]
        )
    )


def show_table_popup():
    return dbc.Modal(
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
    )

def dashboard_data_tab(session_maker):
    datasets_cards = []
    num_of_datasets = None
    with session_maker() as session:
        num_of_datasets = datasets_count(session)
        if num_of_datasets > 0: 
            datasets_cards = [dataset_card(dataset.id, dataset.name) for dataset in get_all_datasets(session)]
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
                dcc.Store(id='deleted_dataset_trigger',data=0),
                dcc.Store(id='added_dataset_trigger',data=0),
                dcc.Store(id='rename_dataset_trigger',data=0),
                html.Div(
                    className='fill-parent-div dashboard__data-tab--datasets-container',
                    id='dataset-cards-container',
                    children=datasets_cards
                ),




                # Pop Ups
                add_dataset_popup(),
                delete_dataset_popup(),
                rename_dataset_popup(),
                show_table_popup(),
                # Data stores
                dcc.Store(id='uploaded_data')
            ]
        )
    )