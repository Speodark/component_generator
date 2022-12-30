from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State
import dash
from dash.exceptions import PreventUpdate
from datetime import datetime
from components import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import (
    get_all_datasets, 
    trace_name_exists, 
    add_trace, 
    traces_count, 
    get_all_traces, 
    get_newest_component, 
    delete_trace,
    component_traces_count
)
from components.charts import charts_dict
import plotly.graph_objects as go

session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))

chart_type_to_class = {
    'line_chart': line_chart,
    'bar_chart': bar_chart
}


@dash.callback(
    Output('create-trace-popup', 'is_open'),
    Output('traces-dataset-dropdown', 'options'),
    Output('new-trace-name-warning', 'children'),
    Output('new-trace-name-warning', 'className'),
    Output('traces-dataset-dropdown', 'value'),
    Output('new-trace-name', 'value'),
    Output('added-trace-trigger','data'),
    Input('add-trace', 'n_clicks'),
    Input('cancel-trace', 'n_clicks'),
    Input('create-trace', 'n_clicks'),
    State('new-trace-name-warning', 'className'),
    State('new-trace-name', 'value'),
    State('components-dropdown', 'value'),
    State('traces-type-dropdown', 'value'),
    State('traces-dataset-dropdown', 'value'),
    prevent_initial_call = True
)
def create_trace_popup(
    _,
    __,
    ___,
    # STATES
    warning_class,
    trace_name,
    component_id,
    trace_type,
    dataset_id
):
    is_open_output = no_update # is the popup open?
    datasets_dropdown_options_output = no_update # update the datasets dropdown value
    warning_text_output = no_update # The warning text
    warning_class_output = no_update # The warning div class
    traces_dataset_dropdown_value = no_update # The value of the datasets dropdown, we need to set to none to restart the choice
    new_trace_name_output = no_update # The new trace name input, to empty when creating new trace
    added_trace_trigger_data_output = no_update # Triggers the rebuild of the traces cards

    triggered = ctx.triggered_id

    if triggered == 'add-trace':
        is_open_output = True
        datasets_dropdown_options_output = []
        with session_maker() as session:
            datasets = get_all_datasets(session)
            datasets_dropdown_options_output = [
                {'label': dataset.name, 'value': dataset.id}
                for dataset in datasets
            ]
    elif triggered == 'cancel-trace':
        is_open_output = False
    elif triggered == 'create-trace':
        # is the name empty?
        if not trace_name:
            warning_text_output = 'You must provide a name'
            warning_class_output = warning_class.replace('hide', '').strip()
        # Is the name longer than 3 characters?
        elif len(trace_name) < 3:
            warning_text_output = 'The name must be 3 characters or more'
            warning_class_output = warning_class.replace('hide', '').strip()
        else:
            # Checks if the name already exists in the database
            name_already_exists = False
            with session_maker() as session:
                name_already_exists = trace_name_exists(component_id, trace_name, session)
            if name_already_exists:
                warning_text_output = 'This name is already taken'
                warning_class_output = warning_class.replace('hide', '').strip()
            else:
                fig_json = getattr(go, trace_type)(name=trace_name).to_plotly_json()
                with session_maker() as session:
                    add_trace(trace_name, component_id, fig_json, session, dataset_id=dataset_id)
                is_open_output = False
                added_trace_trigger_data_output = datetime.now()
                warning_text_output = ''
                warning_class_output = warning_class if 'hide' in warning_class else warning_class + ' hide' 
                traces_dataset_dropdown_value = None
                new_trace_name_output = ''

    return (
        is_open_output,
        datasets_dropdown_options_output,
        warning_text_output, # The warning text
        warning_class_output, # The warning div class
        traces_dataset_dropdown_value,
        new_trace_name_output,
        added_trace_trigger_data_output
    )


# DELETE DATASET CALLBACK
@dash.callback(
    Output('delete-trace-popup', 'is_open'),
    Output('trace_id_to_delete', 'value'),
    Output('deleted_trace_trigger', 'data'),
    Input({'type':'trace_card','id':ALL,'sub_type':'delete'}, 'n_clicks'),
    Input('cancel-trace-delete-btn', 'n_clicks'),
    Input('delete-trace-btn','n_clicks'),
    State('trace_id_to_delete', 'value'),
    State('components-dropdown', 'value'),
    prevent_initial_call = True
)
def delete_dataset_popup(
    n_clicks_trace_cards,
    __,
    ___,
    trace_id_to_delete,
    component_id
):
    is_popup_open = no_update
    trace_id_to_delete_output = no_update
    deleted_trace_trigger = no_update # Triggers the build of the cards container

    triggered_id = ctx.triggered_id
    if triggered_id == 'cancel-trace-delete-btn':
        is_popup_open = False
    elif isinstance(triggered_id, dict) and triggered_id.get('sub_type') and triggered_id.get('sub_type') == 'delete':
        # Prevents update if the n_clicks started the function but wasn't clicked
        # Happens when the card is created
        for input_type in ctx.inputs_list:
            if isinstance(input_type, list) and input_type[0]['id'].get('type') == 'trace_card':
                for index, input_ in enumerate(input_type):
                    if input_['id'] == triggered_id:
                        if n_clicks_trace_cards[index] is None:
                            raise PreventUpdate
        is_popup_open = True
        trace_id_to_delete_output = triggered_id['id']
    elif triggered_id == 'delete-trace-btn':
        with session_maker() as session:
            delete_trace(trace_id_to_delete, session)
            deleted_trace_trigger = component_traces_count(component_id, session) # If i deleted it will never be the same number as before
        
        is_popup_open = False

    return (
        is_popup_open,
        trace_id_to_delete_output,
        deleted_trace_trigger # Triggers the build of the cards container
    )


@dash.callback(
    Output('traces-container', 'children'),
    Input('components-dropdown', 'value'),
    Input('added-trace-trigger','data'),
    Input('deleted_trace_trigger', 'data')
)
def update_traces_container(
    component_id,
    _,
    __
):
    traces_cards = []
    num_of_datasets = None
    with session_maker() as session:
        num_of_datasets = traces_count(session)
        if num_of_datasets > 0: 
            traces_cards = [trace_dataset_card(trace.id, trace.trace_name, 'trace_card') for trace in get_all_traces(component_id, session)]
    
    return traces_cards