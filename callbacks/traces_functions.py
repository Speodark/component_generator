from dash import ctx
from components.charts import charts_dict
from dash.exceptions import PreventUpdate
from utilities.db import (
    get_trace
)

def new_figure_args(trace, trace_dropdowns, trace_inputs):

    def insert_to_dict(new_fig_args, state_type, state_values):
        for index, state_ in enumerate(state_type):
            if state_['id']['arg_name'] in charts_dict[trace.args['type'].capitalize()].args_list:
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