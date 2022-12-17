from whitenoise import WhiteNoise
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from pages.dashboard import dashboard
import vaex

# Generate the app layout
def generateAppLayout():
    return html.Div(
        className="container-page",
        children=[
            dcc.Location(id='url', refresh=False),
            dashboard()
        ]
    )

# initilaize the app
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
# For the heroku deployment
server = app.server
# set the static folder
server.wsgi_app = WhiteNoise(server.wsgi_app, root='assets/')
# title
app.title = 'Component Generator'
# set the layout
app.layout = generateAppLayout

# start the app
if __name__ == "__main__":
    app.run_server(debug=True, port=5050, host="0.0.0.0")