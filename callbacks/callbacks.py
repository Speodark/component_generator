import base64
import io
import dash
from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State
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
@dash.callback(
    Output('graph-fig', 'figure'),
    Output('args-tab', 'children'),
    Input('graph-type', 'value'),
    Input({'type':'input', 'input_type':'text', 'id':ALL}, 'value')
)
def update_chart(chart_type, input_args):

    # Get trigger id
    trigger_id = ctx.triggered_id
    # Get the chart type
    chart_class = chart_type_to_class[chart_type]
    # dictionary of arguments
    args_dictionary = {}
    # Set args tab to be no update incase we change a arg and not the figure type
    args_tab_children = no_update
    if not trigger_id or trigger_id == 'graph-type':
        args_tab_children = [getattr(args, arg)() for arg in chart_class.args]
    else:
        input_lists = ctx.inputs_list
        for input_list in input_lists:
            if input_list and isinstance(input_list, list):
                if input_list[0]['id']['type'] == 'input':
                    for single_input in input_list:
                        if single_input.get('value',None):
                            args_dictionary[single_input['id']['id']] = single_input['value']


    # Create the figure
    figure = chart_class.create_figure()
    figure = chart_class.add_trace(
        fig=figure,
        x = [1,2,3],
        y = [4,5,6],
        args = args_dictionary
    )
    figure = chart_class.add_trace(
        fig=figure,
        x = [1,2,3],
        y = [7,8,9],
        args = args_dictionary
    )

    
    return figure, args_tab_children



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
        html.Div(
            [
                # Display the filename and date
                html.H5(filename),
                html.H6(datetime.fromtimestamp(date)),
                # Display the data as a table
                # html.Table(
                #     # Add the dropdown menus as the first row
                #     [html.Tr([html.Th(dropdown) for dropdown in dropdowns])],
                #     style={'width':'100%'}
                # ),
                # Display the data as an editable data table
                dash_table.DataTable(
                    data=df.to_dict("records"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    sort_action="native",
                    editable=True,
                    page_size=10,
                    page_action="native",
                    style_table={
                        'overflow-x': 'scroll',
                        'width': '100%'
                    },
                    style_cell={
                        'border': '1px solid black',
                        'padding': '5px',
                        'textAlign': 'center'
                    }   
                ),
                html.Button(
                    className='dashboard__load-popup--btn',
                    children='Load data'
                )
            ],
            className='dashboard__load-popup',
        ),
        df
    )


@dash.callback(
    Output('popup', 'children'),
    Input('upload-data', 'contents'),
    State("upload-data", "filename"),
    State("upload-data", "last_modified")
)
def update_table(contents, filename, last_modified):
    if contents is not None and contents != '' and ctx.triggered_id == "upload-data":
        children, df = parse_contents(contents, filename, last_modified)
        return children
    

@dash.callback(
    Output('popup', 'is_open'),
    Input('upload-data', 'contents')
)
def open_popup(contents):
    # Open the popup when a file is uploaded
    return contents is not None