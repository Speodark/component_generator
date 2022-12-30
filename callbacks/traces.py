from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State
import dash
from dash.exceptions import PreventUpdate
from datetime import datetime
from components import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utilities.db import get_all_datasets, trace_name_exists, add_trace, traces_count, get_all_traces, get_newest_component
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

    return (
        is_open_output,
        datasets_dropdown_options_output,
        warning_text_output, # The warning text
        warning_class_output, # The warning div class
        added_trace_trigger_data_output
    )


@dash.callback(
    Output('traces-container', 'children'),
    Input('components-dropdown', 'value'),
    Input('added-trace-trigger','data')
)
def update_traces_container(
    component_id,
    _
):
    traces_cards = []
    num_of_datasets = None
    with session_maker() as session:
        num_of_datasets = traces_count(session)
        if num_of_datasets > 0: 
            traces_cards = [trace_dataset_card(trace.id, trace.trace_name, 'trace_card') for trace in get_all_traces(component_id, session)]
    
    return traces_cards