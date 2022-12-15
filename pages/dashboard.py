import vaex
from dash import html, dcc
from layout import header, sub_header
from components import (
    card,
    category_switch,
    kpi
)
import uuid
from pprint import pprint
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

df = vaex.open("assets/data/ibm-customers.hdf5")

def dashboard():
    return html.Div(
        className='dashboard',
        children=[
            html.Div(
                className='dashboard__filter',
                children=[
                    dcc.Dropdown(
                        ['New York City', 'Montreal', 'San Francisco'],
                        ['Montreal', 'San Francisco'],
                        multi=True
                    ),
                    category_switch('gender', ['Male', 'Female']),
                    category_switch('SeniorCitizen', ['True', 'False']),
                    category_switch('Partner', ['True', 'False']),
                    category_switch('Dependents', ['True', 'False']),
                    category_switch('PhoneService', ['True', 'False']),
                    category_switch('MultipleLines', ['True', 'False']),
                    category_switch('OnlineSecurity', ['True', 'False']),
                    category_switch('OnlineBackup', ['True', 'False']),
                    category_switch('DeviceProtection', ['True', 'False']),
                    category_switch('TechSupport', ['True', 'False']),
                    category_switch('StreamingTV', ['True', 'False']),
                    category_switch('StreamingMovies', ['True', 'False']),
                    category_switch('PaperlessBilling', ['True', 'False']),
                    category_switch('Churn', ['True', 'False']),
                ]
            ),
            html.Div(
                className='dashboard__info',
                children=[
                    kpi(
                        kpi_name='avg_monthly',
                        text='Avg monthly charges',
                        value=300,
                        className='dashboard__info--kpi dashboard__info--kpi__1'
                    ),
                    kpi(
                        kpi_name='total_charges',
                        text='Total Charges',
                        value=3500,
                        className='dashboard__info--kpi dashboard__info--kpi__2'
                    ),
                    dcc.Dropdown(
                        ['New York City', 'Montreal', 'San Francisco'],
                        'Montreal',
                        clearable=False,
                        className='dashboard__info--dd dashboard__info--dd__1'
                    ),
                    dcc.Dropdown(
                        ['New York City', 'Montreal', 'San Francisco'],
                        'Montreal',
                        clearable=False,
                        className='dashboard__info--dd dashboard__info--dd__2'
                    ),
                ]
            )
        ]
    )
