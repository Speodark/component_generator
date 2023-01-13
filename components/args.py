from dash import html,dcc
import dash_mantine_components as dmc
import pandas as pd

class Args:

    ########### VISIBLE ###########
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
                html.Label('Visible:'),
                dcc.Dropdown(
                    options=options,
                    value=options[0]['value'],
                    clearable=False,
                    className='trace-arg__dropdown',
                    id={'type':'trace_arg', 'sub_type':'dropdown', 'arg_name':'visible'},
                )
            ],
        )
    
    ########### SHOWLEGEND ###########
    def showlegend_default(self):
        return [
            {'label': 'True', 'value': True},
            {'label': 'False', 'value': False},
        ]

    def showlegend(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'showlegend'},
            children=[
                html.Label('Show Legend:'),
                dcc.Dropdown(
                    options=self.showlegend_default(),
                    value=self.showlegend_default()[0]['value'],
                    clearable=False,
                    className='trace-arg__dropdown',
                    id={'type':'trace_arg', 'sub_type':'dropdown', 'arg_name':'showlegend'},
                )
            ],
        )
        
    
    ########### SHOWLEGEND ###########
    def legendrank_default(self):
        return 1000

    def legendrank(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'legendrank'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'legendrank'},
                label="Legend Rank:",
                value=self.legendrank_default(),
                style={"width": 200},
                precision=0,
                hideControls = True,
                size='md',
            )
        )


    ########### SHOWLEGEND ###########
    def legendgroup_default(self):
        return ''

    def legendgroup(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'legendgroup'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'legendgroup'},
                label='Legend Group:',
                style={'width':200},
                size='md',
            )
        )

    
    ########### LEGENDGROUPTITLE FONT SIZE ###########
    def legendgrouptitle_font_size_default(self):
        return 0

    def legendgrouptitle_font_size(self):
        return html.Div(
            className='label-item-divider',
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'legendgrouptitle_font_size'},
                label="Size:",
                value=self.legendgrouptitle_font_size_default(),
                style={"width": 200},
                precision=0,
                hideControls = True,
                size='md',
            )
        )


    ########### LEGENDGROUPTITLE FONT FAMILY ###########
    def legendgrouptitle_font_family_default(self):
        return 0

    def legendgrouptitle_font_family(self):
        return html.Div(
            className='label-item-divider',
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'legendgrouptitle_font_family'},
                label='Family:',
                style={'width':200},
                size='md',
            )
        )


    ########### LEGENDGROUPTITLE FONT COLOR ###########
    def legendgrouptitle_font_color_default(self):
        return ''

    def legendgrouptitle_font_color(self):
        return html.Div(
            className='label-item-divider',
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'legendgrouptitle_font_color'},
                label='Font:',
                style={'width':200},
                size='md',
            )
        )


    ########### LEGENDGROUPTITLE Text ###########
    def legendgrouptitle_text_default(self):
        return ''

    def legendgrouptitle_text(self):
        return html.Div(
            className='label-item-divider',
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'legendgrouptitle_text'},
                label='Text:',
                style={'width':200},
                size='md',
            )
        )


    ########### LEGENDGROUPTITLE ###########
    def legendgrouptitle(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'legendgrouptitle'},
            children=[
                html.Label('Legend Group Title:'),
                html.Div(
                    className='trace-arg__container',
                    children=[
                        self.legendgrouptitle_text(),
                        # html.Div(
                        #     className='label-item-divider',
                        #     children=[
                        #         html.Label('Font:'),
                        #         html.Div(
                        #             className='trace-arg__container',
                        #             children=[
                        #                 self.legendgrouptitle_font_color(),
                        #                 self.legendgrouptitle_font_family(),
                        #                 self.legendgrouptitle_font_size()
                        #             ]
                        #         )
                        #     ]
                        # )
                    ]
                )
            ]
        )


        
        
        
        
        