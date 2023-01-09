import dash_mantine_components as dmc
from dash_iconify import DashIconify

import dash
from dash import html, dcc

app = dash.Dash()

app.layout = html.Div([
    dmc.NumberInput(
        label="Your weight in kg",
        value=5,
        style={"width": 200},
        precision=0,
        hideControls = True
    )
])

if __name__ == '__main__':
    app.run_server()
