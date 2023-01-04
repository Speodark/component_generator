from dash import html,dcc
import pandas as pd

class Args:

    def visible_default(self):
        return [
            {'label': 'True', 'value': True},
            {'label': 'False', 'value': False},
            {'label': 'legendonly', 'value': 'legendonly'}
        ]

    def visible(self):
        options = self.visible_default()
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'visible'},
            children=[
                dcc.Dropdown(
                    options=options,
                    value=True,
                    clearable=False,
                    className='trace-arg__dropdown hide',
                    id={'type':'trace_arg', 'sub_type':'dropdown', 'arg_name':'visible'},
                )
            ],
        )
        