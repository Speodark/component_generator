import plotly.graph_objects as go
from dash import html, dcc
from components import Args
import pandas as pd

class Bar(Args):
    # DONT HAVE LEGEND ONLY
    args_list = [
        'name',
        'visible',
        'showlegend',
        'legendrank',
        'legendgroup',
        'legendgrouptitle',
        'legendwidth',
        'opacity',
        'ids',
        'base',
        'width',
        'offset',
        'text',
        'textposition',
        'texttemplate',
        'hovertext',
        'hoverinfo',
        'hovertemplate',
        'xhoverformat',
        'yhoverformat',
        'customdata',
        # Not implemented
        'x0',
        'dx',
        'y0',
        'dy',
        'meta',
        'xaxis',
        'yaxis',
        'orientation',
        'alignmentgroup',
        'offsetgroup',
        'xperiod',
        'xperiodalignment',
        'xperiod0',
        'yperiod',
        'yperiodalignment',
        'yperiod0',
        'marker',
        'textangle',
        'textfont',
        'error_x',
        'error_y',
        'selectedpoints',
        'selected',
        'unselected',
        'cliponaxis',
        'constraintext',
        'hoverlabel',
        'insidetextanchor',
        'insidetextfont',
        'outsidetextfont',
        'xcalendar',
        'ycalendar',
        'uirevision',
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
                        id={'type':'trace_arg', 'sub_type':'dropdown', 'section': 'data', 'arg_name':'x'},
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
                        id={'type':'trace_arg', 'sub_type':'dropdown', 'section': 'data', 'arg_name':'y'},
                    )
                ]
            ),
        ]