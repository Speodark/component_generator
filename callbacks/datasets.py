import base64
import io
import dash
from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State
from dash.exceptions import PreventUpdate
import pandas as pd
from components import *
from datetime import datetime
from pprint import pprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import dataset_name_exists, add_dataset, datasets_count, get_all_datasets, delete_dataset, rename_dataset
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
    Input('upload_file', 'contents'),
    State("upload_file", "filename"),
    State("upload_file", "last_modified"),
    prevent_initial_call=True
)
def update_table(contents, filename, last_modified):
    if contents is not None and contents != '' and ctx.triggered_id == "upload_file":
        children, df = parse_contents(contents, filename, last_modified)
        return children, df.to_dict('records')
    


@dash.callback(
    # the dataset cards container childrens
    Output('dataset-cards-container', 'children'),
    Input('added_dataset_trigger', 'data'),
    Input('deleted_dataset_trigger', 'data'),
    Input('rename_dataset_trigger', 'data'),
    prevent_initial_call=True
)
def update_datasets_container(
    added_trigger,
    deleted_trigger,
    rename_trigger
):
    dataset_cards_container_output = []
    with session_maker() as session:
        num_of_datasets = datasets_count(session)
        if num_of_datasets > 0: 
            dataset_cards_container_output = [dataset_card(dataset.id, dataset.name) for dataset in get_all_datasets(session)]

    return dataset_cards_container_output

    
@dash.callback(
    Output('add-dataset-popup', 'is_open'),
    # Popup component warning
    Output('load-dataset-warning', 'children'),
    Output('load-dataset-warning', 'className'),
    # Number of datasets left
    Output('added_dataset_trigger', 'data'),
    # INPUTS
    Input('upload_file', 'contents'),
    # Cancel the data upload
    Input('load-data-btn', 'n_clicks'),
    # Try and upload the data
    Input('cancel-load-data-btn', 'n_clicks'),
    # STATES
    State('load-dataset-name', 'value'),
    State('uploaded_data', 'data'),
    State('load-dataset-warning', 'className'),
    prevent_initial_call=True
)
def open_add_dataset_popup(
    contents, 
    _,
    __,
    # STATES
    dataset_name,
    uploaded_data, 
    warning_class
):

    # List of output variables
    pop_up_open_output = no_update # is the data upload popup is open
    warning_text_output = no_update # The text for the warning label
    warning_class_output = no_update # The class for the warning label
    added_dataset_trigger = no_update # Triggers the build of the cards container
    
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
                    with session_maker() as session:
                        added_dataset_trigger = datasets_count(session) # If i added it will never be the same number as before
                
                    pop_up_open_output = False 
                    warning_text_output = '' 
                    warning_class_output = warning_class if 'hide' in warning_class else warning_class + ' hide' 

    return (
        pop_up_open_output, # is the data upload popup is open
        warning_text_output, # The text for the warning label
        warning_class_output, # The class for the warning label
        added_dataset_trigger, # Triggers the build of the cards container
    )


# DELETE DATASET CALLBACK
@dash.callback(
    Output('delete-dataset-popup', 'is_open'),
    Output('dataset_id_to_delete', 'value'),
    Output('deleted_dataset_trigger', 'data'),
    Input({'type':'dataset_card','id':ALL,'sub_type':'delete'}, 'n_clicks'),
    Input('cancel-dataset-delete-btn', 'n_clicks'),
    Input('delete-dataset-btn','n_clicks'),
    State('dataset_id_to_delete', 'value'),
    prevent_initial_call = True
)
def delete_dataset_popup(
    n_clicks_dataset_cards,
    __,
    ___,
    dataset_id_to_delete
):
    is_popup_open = no_update
    dataset_id_to_delete_output = no_update
    deleted_dataset_trigger = no_update # Triggers the build of the cards container

    triggered_id = ctx.triggered_id
    if triggered_id == 'cancel-dataset-delete-btn':
        is_popup_open = False
    elif isinstance(triggered_id, dict) and triggered_id.get('sub_type') and triggered_id.get('sub_type') == 'delete':
        # Prevents update if the n_clicks started the function but wasn't clicked
        # Happens when the card is created
        for input_type in ctx.inputs_list:
            if isinstance(input_type, list) and input_type[0]['id'].get('type') == 'dataset_card':
                for index, input_ in enumerate(input_type):
                    if input_['id'] == triggered_id:
                        if n_clicks_dataset_cards[index] is None:
                            raise PreventUpdate
        is_popup_open = True
        dataset_id_to_delete_output = triggered_id['id']
    elif triggered_id == 'delete-dataset-btn':
        with session_maker() as session:
            delete_dataset(dataset_id_to_delete, session)
            deleted_dataset_trigger = datasets_count(session) # If i deleted it will never be the same number as before
        
        is_popup_open = False

    return (
        is_popup_open,
        dataset_id_to_delete_output,
        deleted_dataset_trigger # Triggers the build of the cards container
    )


@dash.callback(
    Output('rename-dataset-popup', 'is_open'),
    # Popup component warning
    Output('rename-dataset-warning', 'children'),
    Output('rename-dataset-warning', 'className'),
    Output('dataset_id_to_rename', 'data'),
    # Number of datasets left
    Output('rename_dataset_trigger', 'data'),
    # INPUTS
    Input({'type':'dataset_card','id':ALL,'sub_type':'rename'}, 'n_clicks'),
    Input('rename-dataset-confirm-btn', 'n_clicks'),
    Input('rename-dataset-cancel-btn', 'n_clicks'),
    # STATES
    State('rename-dataset-input', 'value'),
    State('rename-dataset-warning', 'className'),
    State('dataset_id_to_rename', 'data'),
    prevent_initial_call=True
)
def open_reename_popup(
    n_clicks_dataset_cards, 
    _,
    __,
    # STATES
    dataset_name,
    warning_class,
    dataset_id_to_rename
):

    # List of output variables
    pop_up_open_output = no_update # is the data upload popup is open
    warning_text_output = no_update # The text for the warning label
    warning_class_output = no_update # The class for the warning label
    dataset_id_to_rename_output = no_update # what is the id of the dataset we want to rename
    rename_dataset_trigger = no_update # Triggers the build of the cards container
    
    triggered_id = ctx.triggered_id
    # Close the popup and saves the data.
    if triggered_id == 'rename-dataset-cancel-btn':
        pop_up_open_output = False
    elif isinstance(triggered_id, dict) and triggered_id.get('sub_type') and triggered_id.get('sub_type') == 'rename':
        # Prevents update if the n_clicks started the function but wasn't clicked
        # Happens when the card is created
        for input_type in ctx.inputs_list:
            if isinstance(input_type, list) and input_type[0]['id'].get('type') == 'dataset_card':
                for index, input_ in enumerate(input_type):
                    if input_['id'] == triggered_id:
                        if n_clicks_dataset_cards[index] is None:
                            raise PreventUpdate
        pop_up_open_output = True
        dataset_id_to_rename_output = triggered_id['id']
    elif triggered_id == 'rename-dataset-confirm-btn':
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
                print(dataset_id_to_rename)
                with session_maker() as session:
                    rename_dataset(dataset_id_to_rename, dataset_name, session)
            
                rename_dataset_trigger = datetime.now()
                pop_up_open_output = False 
                warning_text_output = '' 
                warning_class_output = warning_class if 'hide' in warning_class else warning_class + ' hide' 

    return (
        pop_up_open_output, # is the data upload popup is open
        warning_text_output, # The text for the warning label
        warning_class_output, # The class for the warning label
        dataset_id_to_rename_output, # what is the id of the dataset we want to rename
        rename_dataset_trigger, # Triggers the build of the cards container
    )