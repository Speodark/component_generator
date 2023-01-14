from dash import ctx
from components.charts import charts_dict
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import pandas as pd
import copy
from utilities.db import (
    get_trace,
    get_dataset
)


def new_figure_args(trace_type, trace_dropdowns, trace_inputs, trace_inputs_arg_name, sub_type_inputs_error_output):


    def add_to_dict(lst, value, dct):
        for i in range(len(lst) - 1):
            key = lst[i]
            if key in dct:
                dct = dct[key]
            else:
                dct[key] = {}
                dct = dct[key]
        dct[lst[-1]] = value

    # Will only work on inputs (only suppose to work on inputs if its dropdowns then its my problem)
    def is_valid_value(new_fig_args, arg, value):
        temp_dict = copy.deepcopy(new_fig_args)
        if len(arg) > 1:
            add_to_dict(arg, value, temp_dict)
        else:
            temp_dict[arg[0]] = value
        try:
            getattr(go, trace_type)(**temp_dict)
            return True
        except Exception as e:
            print('_'.join(arg))
            sub_type_inputs_error_output[trace_inputs_arg_name.index('_'.join(arg))] = 'Invalid Prop'
            print(e)
            return False

    def insert_to_dict(chart_arg_builder, new_fig_args, state_type, state_values, sub_type):
        for index, state_ in enumerate(state_type):
            arg_placement = state_['id']['arg_name'].split('_')
            arg_name = state_['id']['arg_name']
            # Trying to get the default value for the arg, this is because we have no default for the data
            default_value = getattr(chart_arg_builder, arg_name + "_default", None)
            # If the default arg exists then call the function
            if default_value is not None:
                default_value = default_value()
                # If the default arg is of type dropdown the default value will be in the [0]['value'] position
                if sub_type == 'dropdown':
                    default_value = default_value[0]['value']

            if arg_placement[0] in charts_dict[trace_type].args_list:
                if len(arg_placement) == 1:
                    if default_value != state_values[index]:
                        if is_valid_value(new_fig_args, arg_placement, state_values[index]):
                            new_fig_args[arg_name] = state_values[index]
                else:
                    if default_value != state_values[index]:
                        if is_valid_value(new_fig_args, arg_placement, state_values[index]):
                            add_to_dict(arg_placement, state_values[index], new_fig_args)
        return new_fig_args


    chart_arg_builder = charts_dict[trace_type]()
    new_fig_args = {}
    for state_type in ctx.states_list:
        if isinstance(state_type, list) and state_type:
            if state_type[0]['id'].get('sub_type') == 'dropdown':
                new_fig_args = insert_to_dict(chart_arg_builder, new_fig_args, state_type, trace_dropdowns, 'dropdown')

            elif state_type[0]['id'].get('sub_type') == 'input':
                new_fig_args = insert_to_dict(chart_arg_builder, new_fig_args, state_type, trace_inputs, 'input')
    return new_fig_args


def get_trace_object(session_maker, store_trace_id):
    trace = None
    with session_maker() as session:
        trace = get_trace(store_trace_id, session)
    if not trace:
        print("In the traces callback trace_arguments_popup function somehow the trace is None")
        raise PreventUpdate
    return trace


def update_fig_data(
    choosen_dataset_id,
    trace,
    data_section_dd,
    session_maker,
    update_trace_active_columns,
    store_trace_id,
    fig_data
):
    changed_fig_data = False
    active_columns = {}
    if choosen_dataset_id:
        # if the curreent active_columns of the trace is none i neeed it to be a dict
        current_active_columns = trace.active_columns if trace.active_columns is not None else {}
        if any(x is not None for x in data_section_dd):
            for state_type in ctx.states_list:
                if isinstance(state_type, list) and state_type and state_type[0]['id'].get('section') == 'data':
                    for state_ in state_type:
                        active_columns[state_['id']['arg_name']] = state_['value']
        # Update if the active columns changes
        if current_active_columns != active_columns:
            if None not in data_section_dd:
                with session_maker() as session:
                    df = pd.DataFrame(get_dataset(choosen_dataset_id, session).data)
                    fig_data = {
                        arg_name : df[column_name].tolist()
                        for arg_name, column_name in active_columns.items()
                    }
            changed_fig_data = True
            
    return changed_fig_data, active_columns


def get_fig_data(
    trace,
    session_maker
):
    if trace.dataset_id is not None and trace.active_columns is not None and None not in trace.active_columns.values():
        with session_maker() as session:
            df = pd.DataFrame(get_dataset(trace.dataset_id, session).data)
            fig_data = {
                arg_name : df[column_name].tolist()
                for arg_name, column_name in  trace.active_columns.items()
            }
    else:
        fig_data = {}

    return fig_data