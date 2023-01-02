import plotly.graph_objects as go
from dash import html, dcc

class Bar:
    args_list = [
        'name'
    ]
    
    @staticmethod
    def data_arg():
        return [
            html.Div(
                className='label-item-divider',
                children=[
                    html.Label('Xaxis:'),
                    dcc.Dropdown(
                        options=[],
                        value=None,
                        className='trace-arg__dropdown',
                        id={'type':'trace-arg', 'sub_type':'dropdown', 'arg-name':'x'},
                    )
                ]
            ),
            html.Div(
                className='label-item-divider',
                children=[
                    html.Label('Yaxis:'),
                    dcc.Dropdown(
                        options=[],
                        value=None,
                        className='trace-arg__dropdown',
                        id={'type':'trace-arg', 'sub_type':'dropdown', 'arg-name':'y'},
                    )
                ]
            ),
        ]