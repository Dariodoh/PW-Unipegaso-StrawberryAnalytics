# file: callbacks.py

from dash import Input, Output, State, callback_context, dcc, html, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data import prepare_benchmark_dataframe, PESI_FATTORI

# Importiamo le risorse necessarie
from app import app
from data import get_calendario_colturale_fragola

PRESETS = {
    "btn-preset-tradizionale": {
        'dd-temperatura': 'sub-freddo', 'dd-luce': 'media', 'dd-irrigazione': 'aspersione',
        'dd-fertilizzazione': 'organica', 'dd-patogeni': 'convenzionale', 'dd-frequenza-raccolta': 'media',
        'dd-impollinazione': 'naturale', 'dd-densita': 'bassa', 'dd-umidita': 'alta_rischiosa'
    },
    "btn-preset-soilless": {
        'dd-temperatura': 'ottimale', 'dd-luce': 'alta', 'dd-irrigazione': 'goccia',
        'dd-fertilizzazione': 'idroponica', 'dd-patogeni': 'integrata', 'dd-frequenza-raccolta': 'alta',
        'dd-impollinazione': 'bombi', 'dd-densita': 'alta', 'dd-umidita': 'ottimale'
    },
    "btn-preset-idroponica": {
        'dd-temperatura': 'ottimale', 'dd-luce': 'alta', 'dd-irrigazione': 'goccia',
        'dd-fertilizzazione': 'idroponica', 'dd-patogeni': 'integrata', 'dd-frequenza-raccolta': 'alta',
        'dd-impollinazione': 'bombi', 'dd-densita': 'alta', 'dd-umidita': 'ottimale'
    },
    "btn-preset-sfavorevoli": {
        'dd-temperatura': 'critico', 'dd-luce': 'bassa', 'dd-irrigazione': 'manuale',
        'dd-fertilizzazione': 'organica', 'dd-patogeni': 'convenzionale', 'dd-frequenza-raccolta': 'bassa',
        'dd-impollinazione': 'manuale', 'dd-densita': 'bassa', 'dd-umidita': 'alta_rischiosa'
    },
    "btn-preset-medie": {
        'dd-temperatura': 'sub-caldo', 'dd-luce': 'media', 'dd-irrigazione': 'goccia',
        'dd-fertilizzazione': 'fertirrigazione', 'dd-patogeni': 'integrata', 'dd-frequenza-raccolta': 'media',
        'dd-impollinazione': 'naturale', 'dd-densita': 'media', 'dd-umidita': 'alta_rischiosa'
    },
    "btn-preset-ottimali": {
        'dd-temperatura': 'ottimale', 'dd-luce': 'alta', 'dd-irrigazione': 'goccia',
        'dd-fertilizzazione': 'fertirrigazione', 'dd-patogeni': 'integrata', 'dd-frequenza-raccolta': 'alta',
        'dd-impollinazione': 'bombi', 'dd-densita': 'alta', 'dd-umidita': 'ottimale'
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
    ctx = callback_context
    if not ctx.triggered_id: raise PreventUpdate
    button_id = ctx.triggered_id
    if button_id == "btn-distribuzione-mensile":
        df_calendario = get_calendario_colturale_fragola()
        table_header = html.Thead(html.Tr([html.Th(col) for col in df_calendario.columns]))
        table_body = html.Tbody(
            [html.Tr([html.Td(df_calendario.iloc[i][col]) for col in df_calendario.columns]) for i in
             range(len(df_calendario))])
        tabella = dbc.Table([table_header, table_body], striped=True, bordered=True, hover=True, responsive=True,
                            className="text-center")
        return True, tabella
    if button_id == "btn-chiudi-modale": return False, no_update
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
    ctx = callback_context
    if not ctx.triggered_id: raise PreventUpdate
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
    if button_id == "btn-chiudi-modal-impollinazione": return False, no_update
    return is_open, no_update


@app.callback(
    [Output('dd-temperatura', 'value'), Output('dd-luce', 'value'), Output('dd-irrigazione', 'value'),
     Output('dd-fertilizzazione', 'value'), Output('dd-patogeni', 'value'), Output('dd-frequenza-raccolta', 'value'),
     Output('dd-impollinazione', 'value'), Output('dd-densita', 'value'), Output('dd-umidita', 'value')],
    Input('btn-preset-tradizionale', 'n_clicks'),
    Input('btn-preset-soilless', 'n_clicks'),
    Input('btn-preset-idroponica', 'n_clicks'),
    Input('btn-preset-sfavorevoli', 'n_clicks'),
    Input('btn-preset-medie', 'n_clicks'),
    Input('btn-preset-ottimali', 'n_clicks'),
    prevent_initial_call=True
)
def update_dropdowns_from_preset(*button_clicks):
    ctx = callback_context
    if not ctx.triggered_id: raise PreventUpdate
    button_id = ctx.triggered_id
    if button_id in PRESETS:
        preset_values = PRESETS[button_id]
        return list(preset_values.values())
    return [no_update] * 9


@app.callback(
    Output('grafico-principale', 'figure'),
    Output('testo-spiegazione', 'children'),
    Input('tabs-viste-grafici', 'value'),
    *[Input(id, 'value') for id in PESI_FATTORI.keys()]
)
def update_main_graph(active_tab, *valori_dropdown):
    if active_tab != 'tab-produttivo':
        fig_vuota = go.Figure()
        fig_vuota.update_layout(xaxis={"visible": False}, yaxis={"visible": False}, annotations=[
            {"text": "Seleziona la tab 'Andamento Produttivo'", "xref": "paper", "yref": "paper", "showarrow": False,
             "font": {"size": 20, "color": "#495b52"}}], plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return fig_vuota, "Questa sezione mostra l'andamento produttivo."


    # Step 1: Chiamare la funzione da data.py per ottenere i dati pronti
    fattori = dict(zip(PESI_FATTORI.keys(), valori_dropdown))
    df_plot, produzione_simulata = prepare_benchmark_dataframe(fattori)

    # Step 2: Usare i dati ricevuti per plottare il grafico
    fig = px.bar(df_plot, x='Produzione (kg/m²)', y='Scenario', orientation='h', title='Confronto Produzione Annua Stimata (kg/m²)',
                 text_auto='.2f', color='Scenario',
                 color_discrete_map={'Produzione Stimata': '#d13045', 'Produzione Media': '#7eb671',
                                     'Produzione Ottimale': '#495b52', 'Produzione Sfavorevole': '#f0ad4e'})
    fig.update_layout(xaxis_title='Produzione (kg/m²)',yaxis_title=None,  showlegend=False,
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#495b52'),
                      transition={'duration': 1000, 'easing': 'cubic-in-out'})
    fig.update_traces(textposition='outside',hovertemplate='<b>%{y}</b><br>Produzione: %{x:.2f} kg/m²<extra></extra>')

    # Step 3: Usare il valore ricevuto per creare la spiegazione
    spiegazione = f"""
    Basandosi sui parametri di coltivazione selezionati, la produzione annua stimata è di **{produzione_simulata:.2f} kg/m²**.

    Questo valore si confronta con i seguenti benchmark standard per il settore:
    - **Produzione Ottimale**: 8.50 kg/m² (tipica di impianti ad alta tecnologia).
    - **Produzione Media**: 5.50 kg/m² (risultato comune per aziende ben gestite).
    - **Produzione Sfavorevole**: 3.00 kg/m² (in condizioni di stress o gestione non ideale).

    *Nota: questa è una simulazione basata su un modello. I risultati reali possono variare.*
    """

    return fig, spiegazione