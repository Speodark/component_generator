from dash import html,dcc
import dash_mantine_components as dmc
import pandas as pd

class Args:

    ########### NAME ########### 
    def name_default(self):
        # the name is an unusual case because its a must have and will never be None
        # We need the function for when we check if the value is equal to the default
        # The answer will always be no but in order to not get an error this exists
        return None


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
                min=0,
                hideControls = True,
                size='md'
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
        return None

    def legendgrouptitle_font_family_options(self):
        return [
            {'label': 'Arial', 'value': 'Arial'},
            {'label': 'Balto', 'value': 'Balto'},
            {'label': 'Courier New', 'value': 'Courier New'},
            {'label': 'Droid Sans', 'value': 'Droid Sans'},
            {'label': 'Droid Serif', 'value': 'Droid Serif'},
            {'label': 'Droid Sans Mono', 'value': 'Droid Sans Mono'},
            {'label': 'Gravitas One', 'value': 'Gravitas One'},
            {'label': 'Old Standard TT', 'value': 'Old Standard TT'},
            {'label': 'Open Sans', 'value': 'Open Sans'},
            {'label': 'Overpass', 'value': 'Overpass'},
            {'label': 'PT Sans Narrow', 'value': 'PT Sans Narrow'},
            {'label': 'Raleway', 'value': 'Raleway'},
            {'label': 'Times New Roman', 'value': 'Times New Roman'},
        ]

    def legendgrouptitle_font_family(self):
        return html.Div(
            className='label-item-divider',
            children=[
                html.Label('Size:'),
                dcc.Dropdown(
                    options=self.legendgrouptitle_font_family_options(),
                    value=self.showlegend_default()[0]['value'],
                    clearable=True,
                    className='trace-arg__dropdown',
                    id={'type':'trace_arg', 'sub_type':'multi-dropdown', 'arg_name':'legendgrouptitle_font_family'},
                    multi=True
                )
            ]
        )


    ########### LEGENDGROUPTITLE FONT COLOR ###########
    def legendgrouptitle_font_color_default(self):
        return ''

    def legendgrouptitle_font_color(self):
        return html.Div(
            className='label-item-divider',
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'legendgrouptitle_font_color'},
                label='Color:',
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
                        html.Div(
                            className='label-item-divider',
                            children=[
                                html.Label('Font:'),
                                html.Div(
                                    className='trace-arg__container',
                                    children=[
                                        self.legendgrouptitle_font_color(),
                                        self.legendgrouptitle_font_family(),
                                        self.legendgrouptitle_font_size()
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )


    ########### LEGENDWIDTH ###########
    def legendwidth_default(self):
        return None

    def legendwidth(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'legendwidth'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'legendwidth'},
                label="Legend Width:",
                value=self.legendwidth_default(),
                style={"width": 200},
                precision=0,
                min=0,
                hideControls = True,
                size='md'
            )
        )


    ########### OPACITY ###########
    def opacity_default(self):
        return 1

    def opacity(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'opacity'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'opacity'},
                label="Opacity:",
                value=self.opacity_default(),
                style={"width": 200},
                precision=3,
                min=0,
                max=1,
                hideControls = True,
                size='md'
            )
        )


    ########### IDS ###########
    def ids_default(self):
        return ''

    def ids(self):
        return html.Div(
            className='label-item-divider',
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'arg_name':'ids'},
                label='Text:',
                style={'width':200},
                size='md',
            )
        )
        
        
        
        