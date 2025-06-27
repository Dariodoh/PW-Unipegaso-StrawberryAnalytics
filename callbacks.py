# file: callbacks.py

from dash import Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from dash import html

# Importiamo le risorse necessarie
from app import app
from data import get_calendario_colturale_fragola  # Importiamo la NUOVA funzione


#
# In futuro qui aggiungeremo le altre callback per i grafici e i preset.
#

@app.callback(
    Output("modale-tabella-mensile", "is_open"),
    Output("contenuto-tabella-mensile", "children"),
    [
        Input("btn-distribuzione-mensile", "n_clicks"),
        Input("btn-chiudi-modale", "n_clicks"),
    ],
    [State("modale-tabella-mensile", "is_open")],
    prevent_initial_call=True
)
def toggle_and_fill_modal(n_open, n_close, is_open):
    """
    Apre o chiude il modale. Quando lo apre, lo popola con la tabella
    statica del calendario colturale.
    """
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    # Se il pulsante "Distribuzione Mensile" è stato premuto
    if triggered_id == "btn-distribuzione-mensile":
        # 1. Ottieni il DataFrame del calendario dalla funzione in data.py
        df_calendario = get_calendario_colturale_fragola()

        # 2. Crea la tabella usando Dash Bootstrap Components
        tabella = dbc.Table.from_dataframe(
            df_calendario,
            striped=True,
            bordered=True,
            hover=True,
            responsive=True
        )

        return True, tabella  # Apri il modale e inserisci la tabella

    # Se il pulsante "Chiudi" è stato premuto o il modale era già aperto
    if triggered_id == "btn-chiudi-modale" or is_open:
        return False, None  # Chiudi il modale e non restituire figli

    return is_open, None