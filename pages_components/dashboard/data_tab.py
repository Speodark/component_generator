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
                html.Div(
                    className='dashboard__data--filename',
                    id='current-data-file-name',
                    children='Upload a File'
                ),
                html.Button(
                    id='show-data-table-btn',
                    className='dashboard__load-popup--btn',
                    children='Show Table',
                    disabled=True
                ),
                # Pop Ups
                dbc.Modal(
                    id='popup',
                    size='xl',
                    centered=True,
                    children=[
                        html.Div(
                            id='popup-file-data',
                            className='dashboard__load-popup'
                        ),
                        html.Button(
                            id='load-data-btn',
                            className='dashboard__load-popup--btn',
                            children='Load data'
                        )
                    ],
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