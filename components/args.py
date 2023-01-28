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
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'legendrank'},
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
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'legendgroup'},
                value=self.legendgroup_default(),
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
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'legendgrouptitle_font_size'},
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
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'legendgrouptitle_font_color'},
                value=self.legendgrouptitle_font_color_default(),
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
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'legendgrouptitle_text'},
                value = self.legendgrouptitle_text_default(),
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
        return ''

    def legendwidth(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'legendwidth'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'legendwidth'},
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
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'opacity'},
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


    ########## IDS ###########
    def ids_default(self):
        return ''

    def ids(self):
        return html.Div(
            className='label-item-divider',
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'multi_string', 'arg_name':'ids'},
                value=self.ids_default(),
                label='Ids:',
                style={'width':200},
                size='md',
            )
        )
        
        
    ########### BASE ###########
    def base_default(self):
        return 1

    def base(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'base'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'base'},
                label="Base:",
                value=self.base_default(),
                style={"width": 200},
                hideControls = True,
                size='md'
            )
        )
        
        
    ########### WIDTH ###########
    def width_default(self):
        return ''

    def width(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'width'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'multi_number', 'arg_name':'width'},
                value=self.width_default(),
                label='Width:',
                style={'width':200},
                size='md',
            )
        )


    ########### OFFSET ###########
    def offset_default(self):
        return ''

    def offset(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'offset'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'multi_number', 'arg_name':'offset'},
                value=self.offset_default(),
                label='Offset:',
                style={'width':200},
                size='md',
            )
        )


    ########### TEXT ###########
    def text_default(self):
        return ''

    def text(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'text'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'multi_string', 'arg_name':'text'},
                value=self.text_default(),
                label='Text:',
                style={'width':200},
                size='md',
            )
        )


    ########### TEXTPOSITION ###########
    def textposition_default(self):
        return [
            {'label': 'auto', 'value': 'auto'},
            {'label': 'none', 'value': 'none'},
            {'label': 'outside', 'value': 'outside'},
            {'label': 'inside', 'value': 'inside'},
        ]

    def textposition(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'textposition'},
            children=[
                html.Label('Text Position:'),
                dcc.Dropdown(
                    options=self.textposition_default(),
                    value=self.textposition_default()[0]['value'],
                    clearable=False,
                    className='trace-arg__dropdown',
                    id={'type':'trace_arg', 'sub_type':'dropdown', 'arg_name':'textposition'},
                )
            ],
        )


    ########### TEXTTEMPLATE ###########
    def texttemplate_default(self):
        return ''

    def texttemplate(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'texttemplate'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'multi_string', 'arg_name':'texttemplate'},
                value=self.texttemplate_default(),
                label='Text Template:',
                style={'width':200},
                size='md',
            )
        )


    ########### HOVERTEXT ###########
    def hovertext_default(self):
        return ''

    def hovertext(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'hovertext'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'multi_string', 'arg_name':'hovertext'},
                value=self.hovertext_default(),
                label='Hover Text:',
                style={'width':200},
                size='md',
            )
        )


    ########### HOVERINFO ###########
    def hoverinfo_default(self):
        return [
            {'label': 'all', 'value': 'all'},
            {'label': 'none', 'value': 'none'},
            {'label': 'skip', 'value': 'skip'},
            {'label': 'x', 'value': 'x'},
            {'label': 'y', 'value': 'y'},
            {'label': 'z', 'value': 'z'},
            {'label': 'text', 'value': 'text'},
            {'label': 'name', 'value': 'name'},
            {'label': 'x+y', 'value': 'x+y'},
            {'label': 'x+z', 'value': 'x+z'},
            {'label': 'x+text', 'value': 'x+text'},
            {'label': 'x+name', 'value': 'x+name'},
            {'label': 'y+z', 'value': 'y+z'},
            {'label': 'y+text', 'value': 'y+text'},
            {'label': 'y+name', 'value': 'y+name'},
            {'label': 'z+text', 'value': 'z+text'},
            {'label': 'z+name', 'value': 'z+name'},
            {'label': 'text+name', 'value': 'text+name'},
            {'label': 'x+y+z', 'value': 'x+y+z'},
            {'label': 'x+y+text', 'value': 'x+y+text'},
            {'label': 'x+y+name', 'value': 'x+y+name'},
            {'label': 'x+z+text', 'value': 'x+z+text'},
            {'label': 'x+z+name', 'value': 'x+z+name'},
            {'label': 'x+text+name', 'value': 'x+text+name'},
            {'label': 'y+z+text', 'value': 'y+z+text'},
            {'label': 'y+z+name', 'value': 'y+z+name'},
            {'label': 'y+text+name', 'value': 'y+text+name'},
            {'label': 'z+text+name', 'value': 'z+text+name'},
            {'label': 'x+y+z+text', 'value': 'x+y+z+text'},
            {'label': 'x+y+z+name', 'value': 'x+y+z+name'},
            {'label': 'x+y+text+name', 'value': 'x+y+text+name'},
            {'label': 'x+z+text+name', 'value': 'x+z+text+name'},
            {'label': 'y+z+text+name', 'value': 'y+z+text+name'},
            {'label': 'x+y+z+text+name', 'value': 'x+y+z+text+name'},
        ]

    def hoverinfo(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'hoverinfo'},
            children=[
                html.Label('Hover Info:'),
                dcc.Dropdown(
                    options=self.hoverinfo_default(),
                    value=self.hoverinfo_default()[0]['value'],
                    clearable=False,
                    className='trace-arg__dropdown',
                    id={'type':'trace_arg', 'sub_type':'dropdown', 'arg_name':'hoverinfo'},
                )
            ],
        )


    ########### HOVERTEEMPLATE ###########
    def hovertemplate_default(self):
        return ''

    def hovertemplate(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'hovertemplate'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'multi_string', 'arg_name':'hovertemplate'},
                value=self.hovertemplate_default(),
                label='Hover Template:',
                style={'width':200},
                size='md',
            )
        )


    ########### XHOVERFORMAT ###########
    def xhoverformat_default(self):
        return ''

    def xhoverformat(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'xhoverformat'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'xhoverformat'},
                label='X Hover Format:',
                style={'width':200},
                size='md',
            )
        )


    ########### YHOVERFORMAT ###########
    def yhoverformat_default(self):
        return ''

    def yhoverformat(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'yhoverformat'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'yhoverformat'},
                value=self.yhoverformat_default(),
                label='Y Hover Format:',
                style={'width':200},
                size='md',
            )
        )


    ########### CUSTOMDATA ###########
    def customdata_default(self):
        return ''

    def customdata(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'customdata'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'multi_string', 'arg_name':'customdata'},
                value=self.customdata_default(),
                label='CustomData:',
                style={'width':200},
                size='md',
            )
        )


    ########### XAXIS ###########
    def xaxis_default(self):
        return 'x'

    def xaxis(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'xaxis'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'xaxis'},
                value=self.xaxis_default(),
                label='xaxis:',
                style={'width':200},
                size='md',
            )
        )


    ########### YAXIS ###########
    def yaxis_default(self):
        return 'y'

    def yaxis(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'yaxis'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'yaxis'},
                value=self.yaxis_default(),
                label='yaxis:',
                style={'width':200},
                size='md',
            )
        )


    ########### ORIENTATION ###########
    def orientation_default(self):
        return [
            {'label': 'vertical', 'value': 'v'},
            {'label': 'horizontal', 'value': 'h'},
        ]

    def orientation(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'orientation'},
            children=[
                html.Label('Text Position:'),
                dcc.Dropdown(
                    options=self.orientation_default(),
                    value=self.orientation_default()[0]['value'],
                    clearable=False,
                    className='trace-arg__dropdown',
                    id={'type':'trace_arg', 'sub_type':'dropdown', 'arg_name':'orientation'},
                )
            ],
        )


    ########### ALIGNMENTGROUP ###########
    def alignmentgroup_default(self):
        return ''

    def alignmentgroup(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'alignmentgroup'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'alignmentgroup'},
                value=self.alignmentgroup_default(),
                label='alignmentgroup:',
                style={'width':200},
                size='md',
            )
        )


    ########### OFFSETGROUP ###########
    def offsetgroup_default(self):
        return ''

    def offsetgroup(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'offsetgroup'},
            children=dmc.TextInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'offsetgroup'},
                value=self.offsetgroup_default(),
                label='offsetgroup:',
                style={'width':200},
                size='md',
            )
        )


    ########### XPERIOD ###########
    def xperiod_default(self):
        return 0

    def xperiod(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'xperiod'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'xperiod'},
                label="xperiod:",
                value=self.xperiod_default(),
                style={"width": 200},
                hideControls = True,
                size='md'
            )
        )


    ########### XPERIODALIGNMENT ###########
    def xperiodalignment_default(self):
        return [
            {'label': 'middle', 'value': 'middle'},
            {'label': 'start', 'value': 'start'},
            {'label': 'end', 'value': 'end'},
        ]

    def xperiodalignment(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'xperiodalignment'},
            children=[
                html.Label('X Period Alignment:'),
                dcc.Dropdown(
                    options=self.xperiodalignment_default(),
                    value=self.xperiodalignment_default()[0]['value'],
                    clearable=False,
                    className='trace-arg__dropdown',
                    id={'type':'trace_arg', 'sub_type':'dropdown', 'arg_name':'xperiodalignment'},
                )
            ],
        )


    ########### XPERIOD0 ###########
    def xperiod0_default(self):
        return None

    def xperiod0(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'xperiod0'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'xperiod0'},
                label="xperiod0:",
                value=self.xperiod0_default(),
                style={"width": 200},
                hideControls = True,
                size='md'
            )
        )


    ########### YPERIOD ###########
    def yperiod_default(self):
        return 0

    def yperiod(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'yperiod'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'yperiod'},
                label="yperiod:",
                value=self.yperiod_default(),
                style={"width": 200},
                hideControls = True,
                size='md'
            )
        )


    ########### YPERIODALIGNMENT ###########
    def yperiodalignment_default(self):
        return [
            {'label': 'middle', 'value': 'middle'},
            {'label': 'start', 'value': 'start'},
            {'label': 'end', 'value': 'end'},
        ]

    def yperiodalignment(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'yperiodalignment'},
            children=[
                html.Label('y Period Alignment:'),
                dcc.Dropdown(
                    options=self.yperiodalignment_default(),
                    value=self.yperiodalignment_default()[0]['value'],
                    clearable=False,
                    className='trace-arg__dropdown',
                    id={'type':'trace_arg', 'sub_type':'dropdown', 'arg_name':'yperiodalignment'},
                )
            ],
        )


    ########### YPERIOD0 ###########
    def yperiod0_default(self):
        return None

    def yperiod0(self):
        return html.Div(
            className='label-item-divider',
            id={'type':'trace_arg', 'sub_type':'divider', 'arg_name':'yperiod0'},
            children=dmc.NumberInput(
                id = {'type':'trace_arg', 'sub_type':'input', 'input_type':'default', 'arg_name':'yperiod0'},
                label="yperiod0:",
                value=self.yperiod0_default(),
                style={"width": 200},
                hideControls = True,
                size='md'
            )
        )