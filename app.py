import dash
import dash_bootstrap_components as dbc

# Inizializza l'app Dash con un tema Bootstrap.
# Questa istanza 'app' sarà importata da layout.py e callbacks.py
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX], #Tema Chiaro
    suppress_callback_exceptions=True
)
server = app.server
app.title = "Strawberry Analytics"