from dash import Input, Output, dcc, html, ctx, no_update, ALL, dash_table, State
import dash
from dash.exceptions import PreventUpdate
from components import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

session_maker = sessionmaker(bind=create_engine('sqlite:///utilities/db/models.db'))

chart_type_to_class = {
    'line_chart': line_chart,
    'bar_chart': bar_chart
}


@dash.callback(
    Output('create-trace-popup', 'is_open'),
    Input('add-trace', 'n_clicks'),
    prevent_initial_call = True
)
def create_trace_popup(
    _
):
    return True