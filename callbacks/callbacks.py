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
from utilities.db import component_name_exists, add_component, components_count, get_all_components, delete_component_by_id, rename_component
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



###################################################################################### END
###################################################################################### show table button in the data section

# @dash.callback(
#     Output('show-table-popup', 'is_open'),
#     Output('show-table-popup-children', 'children'),
#     Input('show-data-table-btn', 'n_clicks'),
#     Input('close-show-table-popup', 'n_clicks'),
#     State('current_data', 'data'),
#     State('current_data_name', 'data'),
#     prevent_initial_call=True
# )
# def show_table(_, __, current_data, filename):
#     trigger_id = ctx.triggered_id
#     # Close the popup and saves the data.
#     if trigger_id == 'close-show-table-popup':
#         return False, None

#     df = pd.DataFrame(current_data)
#     return (
#         True,
#         [
#             # Display the filename and date
#             html.H2(
#                 filename,
#                 className='dashboard__load-popup--filename'
#             ),
#             dash_table.DataTable(
#                 data=current_data,
#                 columns=[{"name": i, "id": i} for i in df.columns],
#                 sort_action="native",
#                 editable=False,
#                 cell_selectable=False,
#                 page_size=10,
#                 page_action="native",
#                 style_table={
#                     'overflow-x': 'scroll',
#                     'width': '100%'
#                 },
#             )
#         ]
#     )

