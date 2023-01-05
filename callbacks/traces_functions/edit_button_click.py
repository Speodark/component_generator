from dash import ctx, no_update
from dash.exceptions import PreventUpdate
import pandas as pd
from components.charts import charts_dict

from utilities.db import (
    get_trace,
    get_all_datasets,
    get_dataset
)

def edit_button_click(
    # Regular args
    trace_n_clicks,
    session_maker,
    sub_type_inputs_output,
    sub_type_dropdowns_output,
    trace_inputs_arg_name,
    trace_args_classnames,
    # Output args
    trace_id_args_output,
    datasets_dropdown_options_output,
    datasets_dropdown_value_output,
    data_container_children_output,
    trace_args_classnames_output
):
    triggered_id = ctx.triggered_id
    # Prevents update if the n_clicks started the function but wasn't clicked
    # Happens when the card is created
    for input_type in ctx.inputs_list:
        if (
            isinstance(input_type, list) and 
            input_type and 
            input_type[0]['id'].get('type') == 'trace_card' and 
            input_type[0]['id']['sub_type'] == 'edit'
            ):
            for index, input_ in enumerate(input_type):
                if input_['id'] == triggered_id:
                    if trace_n_clicks[index] is None:
                        raise PreventUpdate

    # Get the trace for later and a list of all the datasets to put in 
    # The dataset dropdown
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


    if trace is None:
        print("In edit button click trace is None weird check this out!")
        raise PreventUpdate


    # If there is a trace I want to update all the arguments to be by that trace
    trace_args = trace.args
    # sub_type_inputs_output[trace_inputs_arg_name.index('name')] = trace.trace_name
    for output in ctx.outputs_list:
        if isinstance(output, list) and output and output[0]['id'].get('sub_type') == 'input':
            arg_name = output[0]['id']['arg_name']
            sub_type_inputs_output[trace_inputs_arg_name.index(arg_name)] = trace_args.get(arg_name, no_update)
        elif isinstance(output, list) and output and output[0]['id'].get('sub_type') == 'dropdown':
            sub_type_dropdowns_output[trace_inputs_arg_name.index(arg_name)] = trace_args.get(arg_name, no_update)

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
        if isinstance(state_type, list) and state_type and state_type[0]['id'].get('sub_type') == 'divider':
            for index, state_ in enumerate(state_type):
                if state_['id']['arg_name'] in charts_dict[trace.args['type'].capitalize()].args_list:
                    trace_args_classnames[index] = trace_args_classnames[index].replace('hide', '')
                else:
                    trace_args_classnames[index] = trace_args_classnames[index] if 'hide' in trace_args_classnames[index] \
                                                    else trace_args_classnames[index] + ' hide'
    trace_args_classnames_output = trace_args_classnames
    

    
    return ( 
        datasets_dropdown_options_output,
        datasets_dropdown_value_output,
        data_container_children_output,
        trace_args_classnames_output
    )
    

        