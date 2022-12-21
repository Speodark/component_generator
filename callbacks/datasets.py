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
from utilities.db import name_exists, add_component, components_count, get_all_components, delete_component_by_id, rename_component
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
            html.H2(
                filename,
                className='dashboard__load-popup--filename'
            ),
            html.H5(
                datetime.fromtimestamp(date),
                className='dashboard__load-popup--date'
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
    Output('popup', 'is_open'),
    Output('current_data', 'data'),
    Output('current_data_name', 'data'),
    Output('current-data-file-name', 'children'),
    Output('show-data-table-btn', 'disabled'),
    Input('upload_file', 'contents'),
    Input('load-data-btn', 'n_clicks'),
    State('uploaded_data', 'data'),
    State('uploaded_data_name', 'data'),
    prevent_initial_call=True
)
def open_popup(contents, n_clicks, uploaded_data, uploaded_data_name):
    trigger_id = ctx.triggered_id
    # Close the popup and saves the data.
    if trigger_id == 'load-data-btn':
        return (
            False, 
            uploaded_data, 
            uploaded_data_name, 
            uploaded_data_name, 
            False
        )
    # Open the popup when a file is uploaded
    return (
        contents is not None, 
        no_update, 
        no_update, 
        no_update, 
        no_update
    )