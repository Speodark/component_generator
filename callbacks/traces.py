from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State, MATCH
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
    component_traces_count,
    get_trace,
    get_dataset,
    update_trace_name,
    update_trace_active_columns,
    update_trace_dataset,
    update_trace
)
from components.charts import charts_dict
import plotly.graph_objects as go
from pprint import pprint
import pandas as pd


session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))


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
    Input('deleted_trace_trigger', 'data'),
    prevent_initial_call = True
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


@dash.callback(
    Output('args-trace-popup', 'is_open'),
    Output('trace_id_args', 'data'),
    Output({'type':'trace_arg', 'sub_type':'input', 'arg_name':ALL}, 'value'),
    Output({'type':'trace_arg', 'sub_type':'input', 'arg_name':ALL}, 'error'),
    Output('trace-arg-dataset-dropdown', 'options'),
    Output('trace-arg-dataset-dropdown', 'value'),
    Output('trace-arg-type-dropdown', 'value'),
    Output('trace-arg-data-container', 'children'),
    Output({'type':'trace_card','id':ALL,'sub_type':'name'},'children'),
    Output('updated_trace_trigger', 'data'),
    Output({'type':'trace_arg', 'sub_type':'divider', 'arg_name':ALL}, 'className'),
    Input({'type':'trace_card','id':ALL,'sub_type':'edit'}, 'n_clicks'),
    Input('close-arg-popup', 'n_clicks'),
    Input('apply-arg-changes','n_clicks'),
    Input('trace-arg-dataset-dropdown', 'value'),
    Input('trace-arg-type-dropdown', 'value'),
    State('trace_id_args','data'),
    State({'type':'trace_arg', 'sub_type':'dropdown', 'section': 'data', 'arg_name':ALL} ,'value'),
    State({'type':'trace_arg', 'sub_type':'input', 'arg_name':ALL}, 'value'),
    State('components-dropdown','value'),
    State({'type':'trace_arg', 'sub_type':'divider', 'arg_name':ALL}, 'className'),
    prevent_initial_call = True
)
def trace_arguments_popup(
    trace_n_clicks,
    _,
    __,
    choosen_dataset_id,
    trace_type,
    # States
    store_trace_id,
    data_section_dd,
    trace_inputs,
    component_id,
    trace_args_classnames
):
    num_sub_type_inputs = 0
    numer_of_trace_cards = 0
    trace_inputs_arg_name = []
    trace_cards_ids_by_order = []
    for output in ctx.outputs_list:
        if isinstance(output, list) and output and output[0]['id'].get('sub_type') == 'input':
            num_sub_type_inputs = len(output)
            for _output in output:
                trace_inputs_arg_name.append(_output['id']['arg_name'])
        elif isinstance(output,list) and output and output[0]['id'].get('type') == 'trace_card' and output[0]['id'].get('sub_type') == 'name':
            numer_of_trace_cards = len(output)
            for _output in output:
                trace_cards_ids_by_order.append(_output['id']['id'])
    popup_is_open_output = no_update # Is the popup open?
    trace_id_args_output = no_update # The id of the trace that opened the popup
    sub_type_inputs_output = [no_update for x in range(num_sub_type_inputs)] # The name of the trace that opened the popup
    sub_type_inputs_error_output = [no_update for x in range(num_sub_type_inputs)] # The text for the error of the name text
    datasets_dropdown_options_output = no_update # the list of available dataset
    datasets_dropdown_value_output = no_update # The value of the current trace
    traces_type_dropdown_value_output = no_update # The graph type of the current trace
    data_container_children_output = no_update # The data requirements for the chart type
    trace_card_name_output = [no_update for x in range(numer_of_trace_cards)] # The names of all the traces cards
    updated_trace_trigger_output = no_update
    trace_args_classnames_output = no_update

    triggered_id = ctx.triggered_id
    # If the close button was clicked
    if triggered_id == 'close-arg-popup':
        popup_is_open_output = False
        trace_id_args_output = None
    # If trigger is the edit button of the trace
    elif (
        isinstance(triggered_id, dict) and 
        triggered_id.get('type') and 
        triggered_id['type'] == 'trace_card' and 
        triggered_id['sub_type'] == 'edit'
        ):
        # Prevents update if the n_clicks started the function but wasn't clicked
        # Happens when the card is created
        for input_type in ctx.inputs_list:
            if isinstance(input_type, list) and input_type and input_type[0]['id'].get('type') == 'trace_card' and input_type[0]['id']['sub_type'] == 'edit':
                for index, input_ in enumerate(input_type):
                    if input_['id'] == triggered_id:
                        if trace_n_clicks[index] is None:
                            raise PreventUpdate

        # Outputs if clicked to open the popup
        popup_is_open_output = True
        trace_id_args_output = triggered_id['id']
        trace = None
        datasets_dropdown_options_output = []
        with session_maker() as session:
            trace = get_trace(trace_id_args_output, session)
            # Datasets list
            datasets = get_all_datasets(session)
            datasets_dropdown_options_output = [
                {'label': dataset.name, 'value': dataset.id}
                for dataset in datasets
            ]

        if trace:
            sub_type_inputs_output[trace_inputs_arg_name.index('name')] = trace.trace_name
            datasets_dropdown_value_output = trace.dataset_id
            traces_type_dropdown_value_output = trace.args['type'].capitalize()
            dataset = None
            if trace.dataset_id:
                with session_maker() as session:
                    dataset = pd.DataFrame(get_dataset(trace.dataset_id, session).data)
            active_columns = trace.active_columns
            data_container_children_output = charts_dict[traces_type_dropdown_value_output].data_arg(dataset, active_columns)

            # Which arguments to show
            for state_type in ctx.states_list:
                if isinstance(state_type, list):
                    print(state_type)
                if isinstance(state_type, list) and state_type and state_type[0]['id'].get('sub_type') == 'divider':
                    for index, state_ in enumerate(state_type):
                        if state_['id']['arg_name'] in charts_dict[trace.args['type'].capitalize()].args_list:
                            trace_args_classnames[index] = trace_args_classnames[index].replace('hide', '')
                        else:
                            trace_args_classnames[index] = trace_args_classnames[index] if 'hide' in trace_args_classnames[index] \
                                                           else trace_args_classnames[index] + ' hide'
            trace_args_classnames_output = trace_args_classnames
    # If the apply button was clicked
    elif triggered_id in ['apply-arg-changes','trace-arg-dataset-dropdown','trace-arg-type-dropdown']:
        # Get the trace
        trace = None
        with session_maker() as session:
            trace = get_trace(store_trace_id, session)
        if not trace:
            print("In the traces callback trace_arguments_popup function somehow the trace is None")
            raise PreventUpdate

        ###### Handle the dataset #####
        if choosen_dataset_id != trace.dataset_id:
            if not choosen_dataset_id:
                data_container_children_output = []
            else:
                dataset = None
                fig_json = getattr(go, trace_type)(name=trace.trace_name).to_plotly_json()
                with session_maker() as session:
                    update_trace(store_trace_id, fig_json, session)
                    update_trace_dataset(trace.id, choosen_dataset_id, session)
                    update_trace_active_columns(store_trace_id, None, session)
                    dataset = pd.DataFrame(get_dataset(choosen_dataset_id, session).data)
                data_container_children_output = charts_dict[trace_type].data_arg(dataset, None)
                updated_trace_trigger_output = datetime.now()
            
        ###### Handle the data #####
        # Get the new active columns
        if choosen_dataset_id:
            current_active_columns = trace.active_columns if trace.active_columns is not None else {}
            active_columns = {}
            if any(x is not None for x in data_section_dd):
                for state_type in ctx.states_list:
                    if isinstance(state_type, list) and state_type and state_type[0]['id'].get('section') == 'data':
                        for index, state_ in enumerate(state_type):
                            active_columns[state_['id']['arg_name']] = state_['value']
            # Update if the active columns changes
            if current_active_columns != active_columns:
                with session_maker() as session:
                    if None not in data_section_dd:
                        df = pd.DataFrame(get_dataset(trace.dataset_id, session).data)
                        fig_data = {
                            arg_name : df[column_name].tolist()
                            for arg_name, column_name in active_columns.items()
                        }
                        fig_json = getattr(go, trace_type)(name=trace.trace_name, **fig_data).to_plotly_json()
                    else:
                        fig_json = getattr(go, trace_type)(name=trace.trace_name).to_plotly_json()
                    update_trace(store_trace_id, fig_json, session)
                    update_trace_active_columns(store_trace_id, active_columns, session)
                updated_trace_trigger_output = datetime.now()


        ###### Handle the name #####
        new_trace_name = trace_inputs[trace_inputs_arg_name.index('name')]
        if new_trace_name != trace.trace_name:
            if not new_trace_name:
                sub_type_inputs_error_output[trace_inputs_arg_name.index('name')] = 'You must provide a name'
            # Is the name longer than 3 characters?
            elif len(new_trace_name) < 3:
                sub_type_inputs_error_output[trace_inputs_arg_name.index('name')] = 'The name must be 3 characters or more'
            else:
                # Checks if the name already exists in the database
                name_already_exists = False
                with session_maker() as session:
                    name_already_exists = trace_name_exists(component_id, new_trace_name, session)
                if name_already_exists:
                    sub_type_inputs_error_output[trace_inputs_arg_name.index('name')] = 'This name is already taken'
                else:
                    with session_maker() as session:
                        update_trace_name(store_trace_id, new_trace_name, session)
                    sub_type_inputs_error_output[trace_inputs_arg_name.index('name')] = None
                    trace_card_name_output[trace_cards_ids_by_order.index(store_trace_id)] = new_trace_name


        ###### Handle the type #####
        current_trace_type = trace.args['type'].capitalize()
        if current_trace_type != trace_type:
            if not trace_type:
                data_container_children_output = []
            else:
                fig_json = getattr(go, trace_type)(name=trace.trace_name).to_plotly_json()
                with session_maker() as session:
                    update_trace(store_trace_id, fig_json, session)
                    update_trace_active_columns(store_trace_id, None, session)
                    dataset = pd.DataFrame(get_dataset(choosen_dataset_id, session).data)
                data_container_children_output = charts_dict[trace_type].data_arg(dataset, None)
                updated_trace_trigger_output = datetime.now()
    return (
        popup_is_open_output,
        trace_id_args_output,
        sub_type_inputs_output,
        sub_type_inputs_error_output,
        datasets_dropdown_options_output,
        datasets_dropdown_value_output,
        traces_type_dropdown_value_output,
        data_container_children_output,
        trace_card_name_output,
        updated_trace_trigger_output,
        trace_args_classnames_output
    )