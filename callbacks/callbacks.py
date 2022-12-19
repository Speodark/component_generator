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
from collections import OrderedDict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import name_exists, add_component, components_count, get_all_components, delete_component_by_id
session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))

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

###################################################################################### Parse and save data callback

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

###################################################################################### END
###################################################################################### show table button in the data section

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

###################################################################################### END
###################################################################################### Add/Delete/Rename Component button
@dash.callback(
    ############################################ Outputs for all situations
    # Components dropdown classname
    Output('components-dropdown', 'className'),
    # Components dropdown options
    Output('components-dropdown', 'options'),
    # Components dropdown options
    Output('components-dropdown', 'value'),
    ############################################ END
    ############################################ Outputs for Add components
    # Pop up
    Output('add-component-popup', 'is_open'),
    # Popup component warning
    Output('add-component-not-available', 'children'),
    Output('add-component-not-available', 'className'),
    # show the dropdown and delete button if they were hidden because there were no components
    Output('open-delete-component-popup', 'className'),
    # Add component button classname
    Output('add-component', 'className'),
    ############################################ END
    ############################################ Outputs for delete components
    # Delete confirm popup
    Output('delete-component-popup', 'is_open'),
    ############################################ END
    ############################################ Inputs for Add components
    # Button to open the popup
    Input('add-component', 'n_clicks'),
    # cancel the component creation and closes the popup
    Input('add-component-cancel-btn', 'n_clicks'),
    # try to create the component and close the popup
    Input('add-component-create-btn', 'n_clicks'),
    ############################################ END
    ############################################ Inputs for Delete components
    # Delete component button to open the delete confirm popup
    Input('open-delete-component-popup', 'n_clicks'),
    Input('delete-component-btn', 'n_clicks'),
    Input('cancel-component-delete-btn', 'n_clicks'),
    ############################################ END
    # The name of the new component
    State('add-component-input', 'value'),
    # The current classname of the popup warning
    State('add-component-not-available', 'className'),
    # The current classnames of thee dropdown and delete button and add component button
    State('open-delete-component-popup', 'className'),
    State('components-dropdown', 'className'),
    State('add-component', 'className'),
    State('components-dropdown', 'className'),
    prevent_initial_call=True
)
def open_add_component_popup(
    _, 
    __, 
    ___, 
    delete_,
    delete__,
    delete___,
    # From here is the states
    name, 
    not_available_classname, 
    delete_component_classname, 
    components_dropdown_classname,
    add_component_btn_classname,
    components_dropdown_value
):
    # All the outputs names, this is done to prevent from making mistakes when returning because the big amount of outputs

    # every button can change the dropdown
    components_dropdown_classname_output = no_update # components dropdown classname 
    components_dropdown_options_output = no_update # The components dropdown options
    components_dropdown_value_output = no_update # The components dropdown value
    # only for the add component button
    pop_up_open_output = no_update # Popup is open?
    warning_text_output = no_update # Warning text
    warning_class_output = no_update # Warning class name
    delete_component_btn_classname_output = no_update # delete component classname
    add_component_btn_classname_output = no_update # The add component btn classname

    # Only for the delete component button
    delete_popup_open_output = no_update # Delete confirm popup is open?

    # Which id triggered the callback
    triggered_id = ctx.triggered_id

    ###################################################################### Add component section
    # If we clicked the add component button
    if triggered_id == 'add-component':
        pop_up_open_output = True
    # If we clickeed the cancel on the popup of the create component
    elif triggered_id == 'add-component-cancel-btn':
        pop_up_open_output = False
        warning_text_output = ''
        warning_class_output = not_available_classname if 'hide' in not_available_classname else not_available_classname + ' hide'
    # If we click on the create button in the create component popup
    elif triggered_id == 'add-component-create-btn':
        # Name checks
        # is the name empty?
        if not name:
            warning_text_output = 'You must provide a name'
            warning_class_output = not_available_classname.replace('hide', '').strip()
        # Is the name longer than 3 characters?
        elif len(name) < 3:
            warning_text_output = 'The name must be 3 characters or more'
            warning_class_output = not_available_classname.replace('hide', '').strip()
        else:
            # Checks if the name already exists in the database
            name_already_exists = False
            with session_maker() as session:
                name_already_exists = name_exists(name, session)
            if name_already_exists:
                warning_text_output = 'This name is already taken'
                warning_class_output = not_available_classname.replace('hide', '').strip()
            else:
                # If all good with the name checks
                # add component
                with session_maker() as session:
                    add_component(name, session)
                new_value = None
                dropdown_options = []
                with session_maker() as session:
                    if components_count(session) > 0:
                        components_list = get_all_components(session)
                        new_value = components_list[0].id
                        dropdown_options = [
                            {'label': c.name, 'value': c.id} 
                            for c in components_list
                        ]
                
                pop_up_open_output = False 
                warning_text_output = '' 
                warning_class_output = not_available_classname if 'hide' in not_available_classname else not_available_classname + ' hide' 
                delete_component_btn_classname_output = delete_component_classname.replace('hide', '').strip() 
                components_dropdown_classname_output = components_dropdown_classname.replace('hide', '').strip() 
                components_dropdown_options_output = dropdown_options 
                components_dropdown_value_output = new_value
                add_component_btn_classname_output = add_component_btn_classname.replace(
                    'dashboard__components--add-component-btn__while-none', 
                    'dashboard__components--add-component-btn'
                ).strip() 
    ###################################################################### END

    ###################################################################### DELETE COMPONENT SECTION
    if triggered_id == 'open-delete-component-popup':
        delete_popup_open_output = True
    elif triggered_id == 'cancel-component-delete-btn':
        delete_popup_open_output = False
    elif triggered_id == 'delete-component-btn':
        delete_popup_open_output = False
        print(components_dropdown_value, 'hello')
        # with session_maker() as session:
        #     add_component(name, session)
        # new_value = None
        # dropdown_options = []
        # with session_maker() as session:
        #     if components_count(session) > 0:
        #         components_list = get_all_components(session)
        #         new_value = components_list[0].id
        #         dropdown_options = [
        #             {'label': c.name, 'value': c.id} 
        #             for c in components_list
        #         ]
    ###################################################################### END

    
    # The order is a must! do not switch around unless you are sure!
    return (
        components_dropdown_classname_output, # components dropdown classname 
        components_dropdown_options_output, # The components dropdown options
        components_dropdown_value_output, # The components dropdown value
        pop_up_open_output, # Popup is open?
        warning_text_output, # Warning text
        warning_class_output, # Warning class name
        delete_component_btn_classname_output, # delete component classname
        add_component_btn_classname_output, # The add component btn classname
        delete_popup_open_output, # is the delete popup open?
    )