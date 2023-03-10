import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc
from utilities.db import get_all_datasets, traces_count, get_all_traces, get_newest_component
from components.charts import charts_dict
from components import trace_dataset_card, Args

args_builder = Args()
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


def arguments_popup():
    return dbc.Modal(
        id='args-trace-popup',
        size='xl',
        centered=True,
        backdrop='static',
        keyboard=False,
        children=[
            dcc.Store(id='trace_id_args'),
            dcc.Store(id='updated_trace_trigger'),
            html.Div(
                className='trace-arg',
                children=[
                    # TABS
                    dmc.Tabs(
                        children=[
                            dmc.TabsList(
                                [
                                    dmc.Tab('Info', value='Info'),
                                    dmc.Tab('Style', value='Style'),
                                    dmc.Tab('Marker', value='Xaxis'),
                                ],
                                grow=True
                            ),
                            dmc.TabsPanel(
                                children=[
                                    # Name arg
                                    dmc.TextInput(
                                        id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'name'},
                                        label='Name:',
                                        style={'width':200},
                                        required=True,
                                        size='md',
                                    ),
                                    # dataset arg
                                    html.Div(
                                        className='label-item-divider',
                                        children=[
                                            html.Label('Datasets:'),
                                            dcc.Dropdown(
                                                options=[],
                                                value=None,
                                                className='trace-arg__dropdown',
                                                id='trace-arg-dataset-dropdown',
                                            )
                                        ]
                                    ),
                                    # type arg
                                    html.Div(
                                        className='label-item-divider',
                                        children=[
                                            html.Label('Type:'),
                                            dcc.Dropdown(
                                                options=[
                                                    {'label': chart_type, 'value': chart_type}
                                                    for chart_type in charts_dict.keys()
                                                ],
                                                value=None,
                                                className='trace-arg__dropdown',
                                                id='trace-arg-type-dropdown',
                                            )
                                        ]
                                    ),
                                    # Data arg
                                    html.Div(
                                        className='label-item-divider',
                                        children=[
                                            html.Label('Data:'),
                                            html.Div(
                                                className='trace-arg__container',
                                                id='trace-arg-data-container',
                                            )
                                        ]
                                    )
                                ], 
                                value='Info',
                                className='trace-arg__info-tab'
                            ),
                            # INFO
                            dmc.TabsPanel(
                                children=[
                                    args_builder.visible(),
                                    args_builder.showlegend(),
                                    args_builder.legendrank(),
                                    args_builder.legendgroup(),
                                    args_builder.legendgrouptitle(),
                                    args_builder.legendwidth(),
                                    args_builder.opacity(),
                                    args_builder.ids(),
                                    args_builder.base(),
                                    args_builder.width(),
                                    args_builder.offset(),
                                    args_builder.text(),
                                    args_builder.textposition(),
                                    args_builder.texttemplate(),
                                    args_builder.hovertext(),
                                    args_builder.hoverinfo(),
                                    args_builder.hovertemplate(),
                                    args_builder.xhoverformat(),
                                    args_builder.yhoverformat(),
                                    args_builder.customdata(),
                                    args_builder.xaxis(),
                                    args_builder.yaxis(),
                                    args_builder.orientation(),
                                    args_builder.alignmentgroup(),
                                    args_builder.offsetgroup(),
                                    args_builder.xperiod(),
                                    args_builder.xperiodalignment(),
                                    args_builder.xperiod0(),
                                    args_builder.yperiod(),
                                    args_builder.yperiodalignment(),
                                    args_builder.yperiod0(),
                                ], 
                                value='Style',
                                className='trace-arg__info-tab'
                            ),
                            dmc.TabsPanel(
                                children=[
                                    
                                ],
                                value='Marker',
                                className='trace-arg__info-tab'
                            ),
                        ],
                        orientation='vertical',
                        placement='left',
                        value='Info',
                        className='trace-arg__tabs'
                    ),
                    # Cancel Button
                    html.Button(
                        id = 'close-arg-popup',
                        className='trace-arg__close-btn',
                        children='X'
                    ),
                    # Submit Button
                    html.Button(
                        id='apply-arg-changes',
                        className='btn__green trace-arg__submit-btn',
                        children='Apply'
                    )
                ]
            )
        ]
    )


def delete_dataset_popup():
    return dbc.Modal(
        id='dont_save_changes_popup',
        size='md',
        centered=True,
        children=html.Div(
            className='dashboard__delete-popup',
            children=[
                html.Span(
                    className='dashboard__delete-popup--title',
                    children='Are you sure you Want to close the window??'
                ),
                html.Span(
                    className='dashboard__delete-popup--warning',
                    children="You haven't applied some of the changes!"
                ),
                # Delete the component
                html.Button(
                    id='dont_save_changes_confirm',
                    className='btn__red dashboard__delete-popup--delete',
                    children='Confirm'
                ),
                # Cancel
                html.Button(
                    id='dont_save_changes_cancel',
                    className='btn__blue dashboard__delete-popup--cancel',
                    children='Cancel'
                ),
            ]
        ),
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
            arguments_popup(),
            delete_dataset_popup()
        ]
    )