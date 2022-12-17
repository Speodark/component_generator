from dash import html,dcc

class args:
    @staticmethod
    def name():
        return html.Div(
            children=[
                html.Span('Trace Name'),
                dcc.Input(
                    id={'type':'input', 'input_type':'text', 'id':'name'}, 
                    type="text",
                    value='',
                    debounce=True,
                    autoComplete='off'
                )
            ],
            className='center_items_vertical'
        )
        
        