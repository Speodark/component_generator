from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State
import dash
from dash.exceptions import PreventUpdate
from components import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import get_all_datasets, trace_name_exists

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
    Input('add-trace', 'n_clicks'),
    Input('cancel-trace', 'n_clicks'),
    Input('create-trace', 'n_clicks'),
    State('new-trace-name-warning', 'className'),
    State('new-trace-name', 'value'),
    State('components-dropdown', 'value'),
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
):
    is_open_output = no_update # is the popup open?
    datasets_dropdown_options_output = no_update # update the datasets dropdown value
    warning_text_output = no_update # The warning text
    warning_class_output = no_update # The warning div class

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
                args_dict = {
                    'name': trace_name
                }
                is_open_output = False

    return (
        is_open_output,
        datasets_dropdown_options_output,
        warning_text_output, # The warning text
        warning_class_output, # The warning div class
    )