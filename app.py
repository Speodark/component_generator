from whitenoise import WhiteNoise
import dash
from dash import html
import dash_bootstrap_components as dbc


TITLE = 'Component Generator'

# Generate the app layout
def layout():
    return html.Div(
        className="container-page",
        children=dash.page_container
    )

# initilaize the app
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
# For the heroku deployment
server = app.server
# set the static folder
server.wsgi_app = WhiteNoise(server.wsgi_app, root='assets/')
# set the layout
app.layout = layout
# Initialize the db session

# start the app
if __name__ == "__main__":
    app.run_server(debug=True, port=5050, host="0.0.0.0")