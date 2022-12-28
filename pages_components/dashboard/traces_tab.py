import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc
from utilities.db import get_all_datasets


def create_trace_popup(session_maker):
    datasets_name_id = []
    with session_maker() as session:
        datasets = get_all_datasets(session)
        datasets_name_id = [
            {'label': dataset.name, 'value': dataset.id}
            for dataset in datasets
        ]
    return dbc.Modal(
        id='create-trace-popup',
        size='lg',
        centered=True,
        children=html.Div(
            className='create-trace',
            children=[
                # TITLE
                html.Span(
                    className='create-trace__title',
                    children='Create Trace'
                ),
                # Trace type dropdown
                html.Div(
                    className='create-trace__type center_items_horizontal',
                    children=[
                        html.Span(
                            className='create-trace__sub-title',
                            children='Trace type'
                        ),
                        html.Span(
                            className='create-trace__spacer',
                            children='-'
                        ),
                        dcc.Dropdown(
                            options=[
                                {'label': 'bar', 'value': 'bar'},
                                {'label': 'line', 'value': 'line'} 
                            ],
                            value='line',
                            className='create-trace__dropdown',
                            id='traces-type-dropdown',
                            clearable=False,
                        )
                    ]
                ),
                # Trace name input
                html.Div(
                    className='create-trace__name center_items_horizontal',
                    children=[
                        html.Span(
                            className='create-trace__sub-title',
                            children='Trace name'
                        ),
                        html.Span(
                            className='create-trace__spacer',
                            children='-'
                        ),
                        dcc.Input(
                            id='new-trace-name',
                            className='create-trace__input',
                            type="text",
                            value='',
                            autoComplete='off'
                        )
                    ]
                ),
                # Trace name warning
                html.Span(
                    id='new-trace-name-warning',
                    className='create-trace__warning hide',
                    children='hello there'
                ),
                # Trace dataset dropdown (can be empty)
                html.Div(
                    className='create-trace__dataset center_items_horizontal',
                    children=[
                        html.Span(
                            className='create-trace__sub-title',
                            children='Trace dataset'
                        ),
                        html.Span(
                            className='create-trace__spacer',
                            children='-'
                        ),
                        dcc.Dropdown(
                            options=datasets_name_id,
                            value=None,
                            className='create-trace__dropdown',
                            id='traces-dataset-dropdown',
                        )
                    ]
                ),
                # Create the trace
                html.Button(
                    id='create-trace',
                    className='btn__green create-trace__create-btn',
                    children='Load'
                ),
                # Cancel the trace creation
                html.Button(
                    id='cancel-trace',
                    className='btn__red create-trace__cancel-btn',
                    children='Cancel'
                )
            ]
        ),
    )


def dashboard_traces_tab(session_maker):
    return dmc.Tab(
        label="Graph Traces", 
        children=html.Div(
            className='center_items_vertical',
            children=[
                html.Div(
                    className='dashboard__traces',
                    children=[]
                ),
                html.Button(
                    id='add-trace',
                    className='btn__blue',
                    children='Add Trace'
                ),
                # POPUPS
                create_trace_popup(session_maker),
            ]
        )
    )