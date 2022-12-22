from dash import html

def dataset_card(id:int ,name: str):
    return html.Div(
        className='dataset-card',
        children=[
            html.Span(
                className='dataset-card__name',
                children=name
            ),
            html.Div(
                className='dataset-card__buttons',
                children=[
                    html.Button(
                        children=html.I(className='eye-icon fa fa-eye'),
                        className='dataset-card__button'
                    ),
                    html.Button(
                        children=html.I(className='pen-icon fa fa-pen'),
                        className='dataset-card__button'
                    ),
                    html.Button(
                        children=html.I(className='trash-icon fa fa-trash'),
                        className='dataset-card__button'
                    )
                ]
            )
        ]
    )