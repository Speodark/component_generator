import plotly.graph_objects as go
from dash import html, dcc
import pandas as pd

class Bar:
    # DONT HAVE LEGEND ONLY
    args_list = [
        'name',
        'visible'
    ]
    
    @staticmethod
    def data_arg(dataset, active_columns):
        options = []
        xaxis_value = None
        yaxis_value = None
        if isinstance(dataset, pd.DataFrame):
            options = dataset.columns
            if active_columns:
                xaxis_value = active_columns['x']
                yaxis_value = active_columns['y']
        return [
            html.Div(
                className='label-item-divider',
                children=[
                    html.Label('Xaxis:'),
                    dcc.Dropdown(
                        options=options,
                        value=xaxis_value,
                        className='trace-arg__dropdown',
                        id={'type':'trace-arg', 'sub_type':'dropdown', 'section': 'data', 'arg-name':'x'},
                    )
                ]
            ),
            html.Div(
                className='label-item-divider',
                children=[
                    html.Label('Yaxis:'),
                    dcc.Dropdown(
                        options=options,
                        value=yaxis_value,
                        className='trace-arg__dropdown',
                        id={'type':'trace-arg', 'sub_type':'dropdown', 'section': 'data', 'arg-name':'y'},
                    )
                ]
            ),
        ]