from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

def dashboard_data_tab():
    return dmc.Tab(
        label="Data", 
        children=html.Div(
            className='center_items_vertical',
            children=[
                dcc.Upload(
                    id='upload_file',
                    children=html.Div(
                        children=[
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]
                    ),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                ),
                # html.Div(
                #     className='dashboard__data--filename',
                #     id='current-data-file-name',
                #     children='Upload a File'
                # ),
                # html.Button(
                #     id='show-data-table-btn',
                #     className='dashboard__load-popup--btn',
                #     children='Show Table',
                #     disabled=True
                # ),
                # Pop Ups
                dbc.Modal(
                    id='add-dataset-popup',
                    size='xl',
                    centered=True,
                    children=html.Div(
                        className='dashboard__data--load-popup',
                        children=[
                            html.Div(
                                id='popup-file-data',
                                className='dashboard__data--load-popup__data'
                            ),
                            html.Div(
                                className='dashboard__data--load-popup__input-container',
                                children=[
                                    html.Span(
                                        className='dashboard__data--load-popup__input-title',
                                        children='Dataset Name - '
                                    ),
                                    # The input for the component name
                                    dcc.Input(
                                        id='load-dataset-name',
                                        className='dashboard__data--load-popup__input',
                                        type="text",
                                        value='',
                                        autoComplete='off'
                                    ),
                                ]
                            ),
                            # If while trying to create a component there's an error this will show the error
                            html.Span(
                                id='load-dataset-warning',
                                className='dashboard__data--load-popup__warning hide',
                                children=''
                            ),
                            # Create the component
                            html.Button(
                                id='load-data-btn',
                                className='btn__green dashboard__data--load-popup__load',
                                children='Load'
                            ),
                            # Cancel the component creation
                            html.Button(
                                id='cancel-load-data-btn',
                                className='btn__red dashboard__data--load-popup__cancel',
                                children='Cancel'
                            )
                        ]
                    )
                ),
                dbc.Modal(
                    id='show-table-popup',
                    size='xl',
                    centered=True,
                    children=[
                        html.Div(
                            id='show-table-popup-children',
                            className='dashboard__show-table-popup'
                        ),
                        html.Button(
                            id='close-show-table-popup',
                            className='btn__red',
                            children='Close'
                        )
                    ],
                ),
                # Data stores
                dcc.Store(id='uploaded_data'),
                dcc.Store(id='uploaded_data_name'),
                dcc.Store(id='current_data'),
                dcc.Store(id='current_data_name'),
            ]
        )
    )