import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc
from utilities.db import get_all_datasets, traces_count, get_all_traces, get_newest_component
from components.charts import charts_dict
from components import trace_dataset_card

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
                dcc.Store(id='added-trace-trigger', data=0),
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
                                {'label': chart_type, 'value': chart_type}
                                for chart_type in charts_dict.keys()
                            ],
                            value=list(charts_dict.keys())[0],
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


def delete_trace_popup():
    return dbc.Modal(
        id='delete-trace-popup',
        size='sm',
        centered=True,
        children=html.Div(
            className='dashboard__delete-popup',
            children=[
                dcc.Store(id='trace_id_to_delete'),
                html.Span(
                    className='dashboard__delete-popup--title',
                    children='Are you sure you want to delete the Trace?'
                ),
                html.Span(
                    className='dashboard__delete-popup--warning',
                    children="You won't be able to retrieve the Trace information!"
                ),
                # Delete the component
                html.Button(
                    id='delete-trace-btn',
                    className='btn__red dashboard__delete-popup--delete',
                    children='Delete'
                ),
                # Cancel
                html.Button(
                    id='cancel-trace-delete-btn',
                    className='btn__blue dashboard__delete-popup--cancel',
                    children='Cancel'
                ),
            ]
        ),
    )


def rename_trace_popup():
    return dbc.Modal(
        id='rename-trace-popup',
        size='lg',
        centered=True,
        children=html.Div(
            className='dashboard__add-component',
            children=[
                dcc.Store(id='trace_id_to_rename'),
                # The popup title
                html.Span(
                    className='dashboard__add-component--title',
                    children='New Name'
                ),
                # The input for the component name
                dcc.Input(
                    id='rename-trace-input',
                    className='dashboard__add-component--input',
                    type="text",
                    value='',
                    autoComplete='off'
                ),
                # If while trying to create a component there's an error this will show the error
                html.Span(
                    id='rename-trace-warning',
                    className='dashboard__add-component--warning hide',
                    children=''
                ),
                # Create the component
                html.Button(
                    id='rename-trace-confirm-btn',
                    className='btn__green dashboard__add-component--create-btn',
                    children='Rename'
                ),
                # Cancel the component creation
                html.Button(
                    id='rename-trace-cancel-btn',
                    className='btn__red dashboard__add-component--cancel-btn',
                    children='Cancel'
                )
            ]
        )
    )


def dashboard_traces_tab(session_maker):
    traces_cards = []
    num_of_datasets = None
    with session_maker() as session:
        num_of_datasets = traces_count(session)
        if num_of_datasets > 0: 
            component_id = get_newest_component(session).id
            traces_cards = [trace_dataset_card(trace.id, trace.trace_name, 'trace_card') for trace in get_all_traces(component_id, session)]
    return html.Div(
        className='center_items_vertical dashboard__traces-tab',
        children=[
            html.Button(
                id='add-trace',
                className='btn__blue',
                children='Add Trace'
            ),
            html.Div(
                className='fill-parent-div dashboard__traces-tab--traces-container',
                id='traces-container',
                children=traces_cards
            ),
            # POPUPS
            create_trace_popup(session_maker),
            dcc.Store(id='deleted_trace_trigger'),
            delete_trace_popup(),
            dcc.Store(id='rename_trace_trigger'),
            rename_trace_popup()
        ]
    )