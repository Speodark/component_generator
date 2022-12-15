from whitenoise import WhiteNoise
import dash
from dash import html, dcc
from pages.dashboard import dashboard
import vaex
from filter_manager import filter_manager

# Generate the app layout
def generateAppLayout():
    return html.Div(
        className="container",
        children=[
            dcc.Location(id='url', refresh=False),
            dashboard()
        ]
    )

# initilaize the app
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True,
)
# For the heroku deployment
server = app.server
# set the static folder
server.wsgi_app = WhiteNoise(server.wsgi_app, root='assets/')
# title
app.title = 'Animal Shelter'
# set the layout
app.layout = generateAppLayout

df = vaex.open("assets/data/ibm-customers.hdf5")
# Starting the filter manager
filter_manager.start(df)
# start the app
if __name__ == "__main__":
    app.run_server(debug=True, port=5050, host="0.0.0.0")