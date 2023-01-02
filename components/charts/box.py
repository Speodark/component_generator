import plotly.graph_objects as go
from dash import html, dcc
import pandas as pd

class Box:

    @staticmethod
    def data_arg(dataset, active_columns):
        options = []
        yaxis_value = None
        if isinstance(dataset, pd.DataFrame):
            options = dataset.columns
            if active_columns:
                yaxis_value = active_columns['y']
        return [
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