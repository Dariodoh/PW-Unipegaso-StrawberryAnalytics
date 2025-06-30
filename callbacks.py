# file: callbacks.py

from dash import Input, Output, State, callback_context, dcc, html
import dash_bootstrap_components as dbc

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
    statica del calendario colturale, costruendola manualmente.
    """
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "btn-distribuzione-mensile":
        # 1. Ottieni il DataFrame del calendario
        df_calendario = get_calendario_colturale_fragola()

        # 2. Crea l'header della tabella (Thead)
        table_header = html.Thead(
            html.Tr([html.Th(col) for col in df_calendario.columns])
        )

        # 3. Crea il corpo della tabella (Tbody)
        # Cicliamo attraverso ogni riga del DataFrame
        table_body = html.Tbody([
            # Per ogni riga, creiamo un html.Tr
            html.Tr([
                # Per ogni cella della riga, creiamo un html.Td
                html.Td(df_calendario.iloc[i][col]) for col in df_calendario.columns
            ]) for i in range(len(df_calendario))
        ])

        # 4. Assembla la tabella completa passando header e body come figli
        tabella = dbc.Table(
            [table_header, table_body],
            striped=True,
            bordered=True,
            hover=True,
            responsive=True
        )

        return True, tabella

    if triggered_id == "btn-chiudi-modale" or is_open:
        return False, None

    return is_open, None

@app.callback(
    Output("modal-info-impollinazione", "is_open"),
    Output("contenuto-info-impollinazione", "children"),
    [
        Input("btn-info-impollinazione", "n_clicks"),
        Input("btn-chiudi-modal-impollinazione", "n_clicks"),
    ],
    [State("modal-info-impollinazione", "is_open")],
    prevent_initial_call=True
)
def toggle_impollinazione_info_modal(n_open, n_close, is_open):
    """
    Apre e chiude il modale informativo sull'impollinazione con bombi.
    """
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "btn-info-impollinazione":
        # Testo estratto e sintetizzato dalle fonti fornite
        testo_informativo = """
        L'impollinazione controllata, specialmente in coltura protetta (serre), è una tecnica fondamentale per garantire un'elevata qualità e uniformità dei frutti.

        Vengono utilizzate arnie di **bombi** (solitamente della specie *Bombus terrestris*) posizionate direttamente tra le coltivazioni. A differenza delle api, i bombi sono impollinatori estremamente efficienti anche a basse temperature e in condizioni di luce non ottimali, tipiche dei periodi di produzione precoce della fragola.

        Questa pratica assicura una fecondazione completa di ogni fiore, che si traduce in:
        *   **Fragole ben formate e di calibro maggiore.**
        *   **Riduzione drastica delle malformazioni.**
        *   **Aumento del valore commerciale e della percentuale di prodotto di prima scelta.**

        Come confermato da diverse realtà lucane nel Metapontino, l'uso dei bombi è ormai uno standard per le produzioni di alta qualità.
        """
        contenuto = dcc.Markdown(testo_informativo)
        return True, contenuto

    if triggered_id == "btn-chiudi-modal-impollinazione" or is_open:
        return False, None

    return is_open, None