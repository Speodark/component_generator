from dash import ctx
from components.charts import charts_dict
from dash.exceptions import PreventUpdate
import pandas as pd
from utilities.db import (
    get_trace,
    get_dataset
)

def new_figure_args(trace_type, trace_dropdowns, trace_inputs):
    def insert_to_dict(new_fig_args, state_type, state_values):
        for index, state_ in enumerate(state_type):
            if state_['id']['arg_name'] in charts_dict[trace_type].args_list:
                new_fig_args[state_['id']['arg_name']] = state_values[index]
        return new_fig_args

    new_fig_args = {}
    for state_type in ctx.states_list:
        if isinstance(state_type, list) and state_type:
            if state_type[0]['id'].get('sub_type') == 'dropdown':
                new_fig_args = insert_to_dict(new_fig_args, state_type, trace_dropdowns)

            elif state_type[0]['id'].get('sub_type') == 'input':
                new_fig_args = insert_to_dict(new_fig_args, state_type, trace_inputs)
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