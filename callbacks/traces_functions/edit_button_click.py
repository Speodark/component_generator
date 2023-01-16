from dash import ctx, no_update
from dash.exceptions import PreventUpdate
import pandas as pd
from components.charts import charts_dict
from components import Args
from utilities.db import (
    get_trace,
    get_all_datasets,
    get_dataset
)

args_builder = Args()

# this function will return the value for the dictionary arguments
def get_value(dictionary, keys):
    for key in keys:
        if key in dictionary:
            dictionary = dictionary[key]
        else:
            return None
    return dictionary


def edit_button_click(
    # Regular args
    trace_n_clicks,
    session_maker,
    sub_type_inputs_output,
    trace_dropdowns_arg_name,
    trace_inputs_arg_name,
    trace_args_classnames,
    # Output args
    sub_type_dropdowns_value_output,
    sub_type_dropdowns_options_output,
    trace_id_args_output,
    datasets_dropdown_options_output,
    datasets_dropdown_value_output,
    data_container_children_output,
    trace_args_classnames_output,
    sub_type_multi_dropdowns_value_output,
    sub_type_multi_dropdowns_options_output,
    trace_multi_dropdowns_arg_name
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

    chart_arg_builder = charts_dict[trace.args['type'].capitalize()]()
    # If there is a trace, I want to update all the arguments to be by that trace
    trace_args = trace.args
    for output in ctx.outputs_list:
        if isinstance(output, list) and output and output[0]['id'].get('sub_type') == 'input':
            for _output in output:
                arg_name = _output['id']['arg_name']
                arg_placement = _output['id']['arg_name'].split('_')
                arg_value = get_value(trace_args, arg_placement)
                if arg_value is None:
                    arg_value = getattr(chart_arg_builder, arg_name + "_default")()
                sub_type_inputs_output[trace_inputs_arg_name.index(arg_name)] = arg_value
        elif isinstance(output, list) and output and output[0]['id'].get('sub_type') == 'dropdown':
            for _output in output:
                arg_name = _output['id']['arg_name']
                arg_options = getattr(chart_arg_builder, arg_name + "_default")()
                arg_placement = _output['id']['arg_name'].split('_')
                arg_value = get_value(trace_args, arg_placement)
                if arg_value is None:
                    sub_type_dropdowns_value_output[trace_dropdowns_arg_name.index(arg_name)] = arg_options[0]['value']
                else:
                    sub_type_dropdowns_value_output[trace_dropdowns_arg_name.index(arg_name)] = arg_value
                sub_type_dropdowns_options_output[trace_dropdowns_arg_name.index(arg_name)] = arg_options
        elif isinstance(output, list) and output and output[0]['id'].get('sub_type') == 'multi-dropdown':
            for _output in output:
                arg_name = _output['id']['arg_name']
                arg_options = getattr(chart_arg_builder, arg_name + "_options")()
                arg_default = getattr(chart_arg_builder, arg_name + "_default")()
                arg_placement = _output['id']['arg_name'].split('_')
                arg_value = get_value(trace_args, arg_placement)
                if arg_value is None:
                    sub_type_multi_dropdowns_value_output[trace_multi_dropdowns_arg_name.index(arg_name)] = arg_default
                else:
                    sub_type_multi_dropdowns_value_output[trace_multi_dropdowns_arg_name.index(arg_name)] = arg_value
                sub_type_multi_dropdowns_options_output[trace_multi_dropdowns_arg_name.index(arg_name)] = arg_options

    datasets_dropdown_value_output = trace.dataset_id
    trace_type_dropdown_value_output = trace.args['type'].capitalize()

    # Handle data container childrens
    if not trace.dataset_id and not trace_type_dropdown_value_output:
        data_container_children_output = "Choose a dataset and a trace type!"
    elif not trace.dataset_id:
        data_container_children_output = "Choose a dataset!"
    elif not trace_type_dropdown_value_output:
        data_container_children_output = "Choose a Type!"
    else:
        dataset = None
        with session_maker() as session:
            dataset = pd.DataFrame(get_dataset(trace.dataset_id, session).data)
        active_columns = trace.active_columns
        data_container_children_output = charts_dict[trace_type_dropdown_value_output].data_arg(dataset, active_columns)

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
        trace_args_classnames_output,
        trace_type_dropdown_value_output
    )
    

        