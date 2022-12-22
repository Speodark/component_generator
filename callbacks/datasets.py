import base64
import io
import dash
from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State
import pandas as pd
from components import *
from datetime import datetime
from pprint import pprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import dataset_name_exists, add_dataset, datasets_count, get_all_datasets
from components import dataset_card
session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))


def parse_contents(contents, filename, date):
    # Split the content string into the content type and the data
    content_type, content_string = contents.split(",")
    # Decode the data from base64
    decoded = base64.b64decode(content_string)
    # Calculate the size of the file in bytes
    sizeInBytes = len(content_string) * 3 / 4 - content_string.count('=')

    try:
        # Read the data from the uploaded file
        if '.xlsx' in filename:
            # Use the pd.read_excel() method for Excel files
            df = pd.read_excel(io.BytesIO(decoded), nrows=2000)
        elif '.csv' in filename:
            # Use the pd.read_csv() method for CSV files
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), nrows=2000)
        elif '.hdf5' in filename:
            # Return an error message if the file is an HDF5 file
            return html.Div(["hdf5 not supported yet"]), None

    except Exception as e:
        # Print the error message if there was a problem reading the file
        print(e)
        return html.Div(["There was an error processing this file."]), None

    # Create a dropdown menu for each column in the dataframe
    dropdowns = []
    for col in df.columns:
        dropdown = dcc.Dropdown(
            id=f'dropdown-{col}',
            options=[
                {'label': 'str', 'value': 'str'},
                {'label': 'bool', 'value': 'bool'},
                {'label': 'int', 'value': 'int'},
                {'label': 'float', 'value': 'float'},
                {'label': 'date', 'value': 'date'}
            ],
            value='str',
            clearable=False
        )
        dropdowns.append(dropdown)
    # Return the contents of the file as a table and a dataframe
    return (
        [
            # Display the filename and date
            html.Div(
                className='dashboard__data--load-popup__data--title',
                children=[
                    html.Span(
                        filename,
                    ),
                    html.Span('-'),
                    html.Span(
                        datetime.fromtimestamp(date),
                    )
                ]
            ),
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                sort_action="native",
                editable=False,
                cell_selectable=False,
                page_size=10,
                page_action="native",
                style_table={
                    'overflow-x': 'scroll',
                    'width': '100%'
                },
            )
        ],
        df
    )


@dash.callback(
    Output('popup-file-data', 'children'),
    Output('uploaded_data', 'data'),
    Output('uploaded_data_name', 'data'),
    Input('upload_file', 'contents'),
    State("upload_file", "filename"),
    State("upload_file", "last_modified"),
    prevent_initial_call=True
)
def update_table(contents, filename, last_modified):
    if contents is not None and contents != '' and ctx.triggered_id == "upload_file":
        children, df = parse_contents(contents, filename, last_modified)
        return children, df.to_dict('records'), filename
    

@dash.callback(
    Output('add-dataset-popup', 'is_open'),
    # Popup component warning
    Output('load-dataset-warning', 'children'),
    Output('load-dataset-warning', 'className'),
    # the dataset cards container childrens
    Output('dataset-cards-container', 'children'),
    # INPUTS
    Input('upload_file', 'contents'),
    # Cancel the data upload
    Input('load-data-btn', 'n_clicks'),
    # Try and upload the data
    Input('cancel-load-data-btn', 'n_clicks'),
    # STATES
    State('load-dataset-name', 'value'),
    State('uploaded_data', 'data'),
    State('uploaded_data_name', 'data'),
    State('load-dataset-warning', 'className'),
    prevent_initial_call=True
)
def open_popup(
    contents, 
    _,
    __,
    # STATES
    dataset_name,
    uploaded_data, 
    uploaded_data_name,
    warning_class
):

    # List of output variables
    pop_up_open_output = no_update # is the data upload popup is open
    warning_text_output = no_update # The text for the warning label
    warning_class_output = no_update # The class for the warning label
    dataset_cards_container_output = no_update # The childrens for the dataset cards container
    
    trigger_id = ctx.triggered_id
    # Close the popup and saves the data.
    if trigger_id == 'upload_file':
        pop_up_open_output = contents is not None
    elif trigger_id == 'cancel-load-data-btn':
        pop_up_open_output = False
    elif trigger_id == 'load-data-btn':
        if contents is None:
            pop_up_open_output = False
        else:
            # is the name empty?
            if not dataset_name:
                warning_text_output = 'You must provide a name'
                warning_class_output = warning_class.replace('hide', '').strip()
            # Is the name longer than 3 characters?
            elif len(dataset_name) < 3:
                warning_text_output = 'The name must be 3 characters or more'
                warning_class_output = warning_class.replace('hide', '').strip()
            else:
                # Checks if the name already exists in the database
                name_already_exists = False
                with session_maker() as session:
                    name_already_exists = dataset_name_exists(dataset_name, session)
                if name_already_exists:
                    warning_text_output = 'This name is already taken'
                    warning_class_output = warning_class.replace('hide', '').strip()
                else:
                    # If all good with the name checks
                    # add dataset
                    with session_maker() as session:
                        add_dataset(dataset_name, uploaded_data, session)
                    dataset_cards_container_output = []
                    with session_maker() as session:
                        num_of_datasets = datasets_count(session)
                        if num_of_datasets > 0: 
                            dataset_cards_container_output = [dataset_card(dataset.id, dataset.name) for dataset in get_all_datasets(session)]
                
                    pop_up_open_output = False 
                    warning_text_output = '' 
                    warning_class_output = warning_class if 'hide' in warning_class else warning_class + ' hide' 

    return (
        pop_up_open_output, # is the data upload popup is open
        warning_text_output, # The text for the warning label
        warning_class_output, # The class for the warning label
        dataset_cards_container_output, # The childrens for the dataset cards container
    )