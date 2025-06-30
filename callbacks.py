# file: callbacks.py

from dash import Input, Output, State, callback_context, dcc, html, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Importiamo le risorse necessarie
from app import app
from data import get_calendario_colturale_fragola  # Importiamo la NUOVA funzione


PRESETS = {
    # Preset per tipo di coltura
    "btn-preset-tradizionale": {
        'dd-temperatura': 'medium', 'dd-luce': 'medium', 'dd-umidita': 'medium',
        'dd-irrigazione': 'medium', 'dd-fertilizzazione': 'low', 'dd-patogeni': 'medium',
        'dd-impollinazione': 'low', 'dd-densita': 'medium', 'dd-frequenza-raccolta': 'medium'
    },
    "btn-preset-soilless": {
        'dd-temperatura': 'high', 'dd-luce': 'high', 'dd-umidita': 'high',
        'dd-irrigazione': 'high', 'dd-fertilizzazione': 'high', 'dd-patogeni': 'low',
        'dd-impollinazione': 'high', 'dd-densita': 'high', 'dd-frequenza-raccolta': 'high'
    },
    "btn-preset-idroponica": {
        'dd-temperatura': 'high', 'dd-luce': 'high', 'dd-umidita': 'high',
        'dd-irrigazione': 'high', 'dd-fertilizzazione': 'high', 'dd-patogeni': 'low',
        'dd-impollinazione': 'high', 'dd-densita': 'high',  'dd-frequenza-raccolta': 'high'
    },
    # Preset per condizioni
    "btn-preset-sfavorevoli": {
        'dd-temperatura': 'low', 'dd-luce': 'low', 'dd-umidita': 'low',
        'dd-irrigazione': 'low', 'dd-fertilizzazione': 'low', 'dd-patogeni': 'high',
        'dd-impollinazione': 'low', 'dd-densita': 'low', 'dd-frequenza-raccolta': 'low'
    },
    "btn-preset-medie": {
        'dd-temperatura': 'medium', 'dd-luce': 'medium', 'dd-umidita': 'medium',
        'dd-irrigazione': 'medium', 'dd-fertilizzazione': 'medium', 'dd-patogeni': 'medium',
        'dd-impollinazione': 'medium', 'dd-densita': 'medium', 'dd-frequenza-raccolta': 'medium'
    },
    "btn-preset-ottimali": {
        'dd-temperatura': 'high', 'dd-luce': 'high', 'dd-umidita': 'high',
        'dd-irrigazione': 'high', 'dd-fertilizzazione': 'high', 'dd-patogeni': 'low',
        'dd-impollinazione': 'high', 'dd-densita': 'high', 'dd-frequenza-raccolta': 'high'
    }
}

@app.callback(
    Output("modale-tabella-mensile", "is_open"),
    Output("contenuto-tabella-mensile", "children"),
    Input("btn-distribuzione-mensile", "n_clicks"),
    Input("btn-chiudi-modale", "n_clicks"),
    State("modale-tabella-mensile", "is_open"),
    prevent_initial_call=True
)
def toggle_and_fill_modal(n_open, n_close, is_open):
    """
    Apre o chiude il modale. Quando lo apre, lo popola con la tabella
    statica del calendario colturale, costruendola manualmente.
    """
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    button_id = ctx.triggered_id

    if button_id == "btn-distribuzione-mensile":
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
            responsive=True,
            className="text-center"
        )

        return True, tabella

    if button_id == "btn-chiudi-modale" :
        return False, no_update

    return is_open, no_update

@app.callback(
    Output("modal-info-impollinazione", "is_open"),
    Output("contenuto-info-impollinazione", "children"),
    Input("btn-info-impollinazione", "n_clicks"),
    Input("btn-chiudi-modal-impollinazione", "n_clicks"),
    State("modal-info-impollinazione", "is_open"),
    prevent_initial_call=True
)
def toggle_impollinazione_info_modal(n_open, n_close, is_open):
    """
    Apre e chiude il modale informativo sull'impollinazione con bombi.
    """
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    button_id = ctx.triggered_id

    if button_id == "btn-info-impollinazione":
        testo_informativo = """
        L'impollinazione controllata, specialmente in coltura protetta (serre), è una tecnica fondamentale per garantire un'elevata qualità e uniformità dei frutti.

        Vengono utilizzate arnie di **bombi** (solitamente della specie *Bombus terrestris*) posizionate direttamente tra le coltivazioni. A differenza delle api, i bombi sono impollinatori estremamente efficienti anche a basse temperature e in condizioni di luce non ottimali, tipiche dei periodi di produzione precoce della fragola.

        Questa pratica assicura una fecondazione completa di ogni fiore, che si traduce in:
        *   **Fragole ben formate e di calibro maggiore.**
        *   **Riduzione drastica delle malformazioni.**
        *   **Aumento del valore commerciale e della percentuale di prodotto di prima scelta.**

        Come confermato da diverse realtà lucane nel Metapontino, l'uso dei bombi è ormai uno standard per le produzioni di alta qualità.
        """
        contenuto = dcc.Markdown(testo_informativo, style={'textAlign': 'justify'})
        return True, contenuto

    if button_id == "btn-chiudi-modal-impollinazione":
        return False, no_update

    return is_open, no_update

@app.callback(
    # L'Output è una lista di tutti i valori dei 9 dropdown
    [
        Output('dd-temperatura', 'value'),
        Output('dd-luce', 'value'),
        Output('dd-umidita', 'value'),
        Output('dd-irrigazione', 'value'),
        Output('dd-fertilizzazione', 'value'),
        Output('dd-patogeni', 'value'),
        Output('dd-impollinazione', 'value'),
        Output('dd-densita', 'value'),
        Output('dd-frequenza-raccolta', 'value')
    ],
    [
        Input('btn-preset-tradizionale', 'n_clicks'),
        Input('btn-preset-soilless', 'n_clicks'),
        Input('btn-preset-idroponica', 'n_clicks'),
        Input('btn-preset-sfavorevoli', 'n_clicks'),
        Input('btn-preset-medie', 'n_clicks'),
        Input('btn-preset-ottimali', 'n_clicks')
    ],
    prevent_initial_call=True
)
def update_dropdowns_from_preset(*button_clicks):
    """
    Questa callback si attiva quando uno qualsiasi dei 6 pulsanti di preset viene cliccato.
    Usa il context per identificare quale pulsante è stato premuto, cerca i valori
    corrispondenti nel dizionario PRESETS e li usa per aggiornare tutti i 9 dropdown.
    """
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    button_id = ctx.triggered_id

    # Controlla se il pulsante cliccato è uno dei nostri preset
    if button_id in PRESETS:
        # Recupera il dizionario di valori per quel preset
        preset_values = PRESETS[button_id]
        # Restituisce la lista di valori. L'ordine è garantito
        # e corrisponderà all'ordine degli Output nel decoratore.
        return list(preset_values.values())

    # Se per qualche motivo l'ID non è nei preset, non fare nulla
    return [no_update] * 9