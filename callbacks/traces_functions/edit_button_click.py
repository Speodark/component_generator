from dash import ctx
from dash.exceptions import PreventUpdate
import pandas as pd
from components.charts import charts_dict

from utilities.db import (
    get_trace,
    get_all_datasets,
    get_dataset
)

def edit_button_click(
    trace_n_clicks,
    session_maker,
    sub_type_inputs_output,
    trace_inputs_arg_name,
    trace_args_classnames
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
            if isinstance(state_type, list) and state_type and state_type[0]['id'].get('sub_type') == 'divider':
                for index, state_ in enumerate(state_type):
                    if state_['id']['arg_name'] in charts_dict[trace.args['type'].capitalize()].args_list:
                        trace_args_classnames[index] = trace_args_classnames[index].replace('hide', '')
                    else:
                        trace_args_classnames[index] = trace_args_classnames[index] if 'hide' in trace_args_classnames[index] \
                                                        else trace_args_classnames[index] + ' hide'
        trace_args_classnames_output = trace_args_classnames

        