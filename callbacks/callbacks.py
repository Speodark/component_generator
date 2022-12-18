import base64
import io
import dash
from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
from components import *
from datetime import datetime
import os
import h5py
from pprint import pprint
import numpy as np


chart_type_to_class = {
    'line_chart': line_chart,
    'bar_chart': bar_chart
}
# @dash.callback(
#     Output('graph-fig', 'figure'),
#     Output('args-tab', 'children'),
#     Input('graph-type', 'value'),
#     Input({'type':'input', 'input_type':'text', 'id':ALL}, 'value')
# )
# def update_chart(chart_type, input_args):
#     # Get trigger id
#     trigger_id = ctx.triggered_id
#     # Get the chart type
#     chart_class = chart_type_to_class[chart_type]
#     # dictionary of arguments
#     args_dictionary = {}
#     # Set args tab to be no update incase we change a arg and not the figure type
#     args_tab_children = no_update
#     if not trigger_id or trigger_id == 'graph-type':
#         args_tab_children = [getattr(args, arg)() for arg in chart_class.args]
#     else:
#         input_lists = ctx.inputs_list
#         for input_list in input_lists:
#             if input_list and isinstance(input_list, list):
#                 if input_list[0]['id']['type'] == 'input':
#                     for single_input in input_list:
#                         if single_input.get('value',None):
#                             args_dictionary[single_input['id']['id']] = single_input['value']


#     # Create the figure
#     figure = chart_class.create_figure()
#     figure = chart_class.add_trace(
#         fig=figure,
#         x = [1,2,3],
#         y = [4,5,6],
#         args = args_dictionary
#     )
#     figure = chart_class.add_trace(
#         fig=figure,
#         x = [1,2,3],
#         y = [7,8,9],
#         args = args_dictionary
#     )

    
#     return figure, args_tab_children



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


@dash.callback(
    Output('show-table-popup', 'is_open'),
    Output('show-table-popup-children', 'children'),
    Input('show-data-table-btn', 'n_clicks'),
    Input('close-show-table-popup', 'n_clicks'),
    State('current_data', 'data'),
    State('current_data_name', 'data'),
    prevent_initial_call=True
)
def show_table(_, __, current_data, filename):
    trigger_id = ctx.triggered_id
    # Close the popup and saves the data.
    if trigger_id == 'close-show-table-popup':
        return False, None

    df = pd.DataFrame(current_data)
    return (
        True,
        [
            # Display the filename and date
            html.H2(
                filename,
                className='dashboard__load-popup--filename'
            ),
            dash_table.DataTable(
                data=current_data,
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
        ]
    )