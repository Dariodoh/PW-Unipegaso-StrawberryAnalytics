# file: callbacks.py

from dash import Input, Output, State, callback_context, dcc, html, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data import prepare_benchmark_dataframe, simula_consumo_risorse, PESI_FATTORI

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
    # Aggiorniamo le figure
    Output('grafico-produttivo', 'figure'),
    Output('grafico-risorse', 'figure'),
    Output('grafico-finanziario', 'figure'),
    # Aggiorniamo la visibilità (stile)
    Output('grafico-produttivo', 'style'),
    Output('grafico-risorse', 'style'),
    Output('grafico-finanziario', 'style'),
    # Aggiorniamo la spiegazione
    Output('testo-spiegazione', 'children'),
    Input('tabs-viste-grafici', 'value'),
    *[Input(id, 'value') for id in PESI_FATTORI.keys()]
)
def update_main_view(active_tab, *valori_dropdown):
    fattori = dict(zip(PESI_FATTORI.keys(), valori_dropdown))

    # Stili di default: tutti nascosti
    style_prod = {'display': 'none', 'height': '50vh'}
    style_risorse = {'display': 'none', 'height': '50vh'}
    style_fin = {'display': 'none', 'height': '50vh'}

    if active_tab == 'tab-produttivo':
        df_plot, produzione_simulata = prepare_benchmark_dataframe(fattori)
        fig = px.bar(
            df_plot, x='Produzione (kg/m²)', y='Scenario', orientation='h',
            title='Confronto Produzione Annua Stimata (kg/m²)', text_auto='.2f', color='Scenario',
            color_discrete_map={'Produzione Stimata': '#d13045', 'Produzione Media': '#7eb671',
                                'Produzione Ottimale': '#495b52', 'Produzione Sfavorevole': '#f0ad4e'}
        )
        fig.update_layout(xaxis_title='Produzione (kg/m²)', yaxis_title=None, showlegend=False,
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#495b52'),
                          transition={'duration': 500, 'easing': 'cubic-in-out'},
                          title_x=0.5,
                          title_xanchor='center'
                          )
        fig.update_traces(textposition='outside',
                          hovertemplate='<b>%{y}</b><br>Produzione: %{x:.2f} kg/m²<extra></extra>')
        spiegazione = f"""
        Basandosi sui parametri di coltivazione selezionati, la produzione annua stimata è di **{produzione_simulata:.2f} kg/m²**.
    
        Questo valore si confronta con i seguenti benchmark standard per il settore:
        - **Produzione Ottimale**: 8.50 kg/m² (tipica di impianti ad alta tecnologia).
        - **Produzione Media**: 5.50 kg/m² (risultato comune per aziende ben gestite).
        - **Produzione Sfavorevole**: 3.00 kg/m² (in condizioni di stress o gestione non ideale).
    
        *Nota: questa è una simulazione basata su un modello. I risultati reali possono variare.*
        """

        style_prod['display'] = 'block'  # Rendiamo visibile solo questo
        return fig, no_update, no_update, style_prod, style_risorse, style_fin, spiegazione

        # --- TAB: USO DELLE RISORSE ---
    elif active_tab == 'tab-risorse':
        consumi_stimati, benchmark_ottimali = simula_consumo_risorse(fattori)
        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'indicator'}, {'type': 'indicator'}]],
                            subplot_titles=('Acqua (l/m²)', 'Fertilizzanti (kg/m²)'))
        fig.add_trace(go.Indicator(mode="gauge+number", value=consumi_stimati['acqua'],
                                   gauge={'axis': {'range': [None, 1250]}, 'bar': {'color': "#d13045"},
                                          'steps': [{'range': [0, 550], 'color': "#7eb671"},
                                                    {'range': [550, 750], 'color': "gold"}],
                                          'threshold': {'value': 500}}), row=1, col=1)
        fig.add_trace(
            go.Indicator(mode="gauge+number", value=consumi_stimati['fertilizzanti'], number={'valueformat': '.3f'},
                         gauge={'axis': {'range': [None, 0.175]}, 'bar': {'color': "#d13045"},
                                'steps': [{'range': [0, 0.077], 'color': "#7eb671"},
                                          {'range': [0.077, 0.105], 'color': "gold"}], 'threshold': {'value': 0.07}}),
            row=1, col=2)
        fig.update_layout(title_text="Stima del Consumo di Risorse vs. Ottimale", plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#495b52'),
                          transition={'duration': 500, 'easing': 'cubic-in-out'},
                          title_x=0.5,
                          title_xanchor='center'
                          )
        spiegazione = f"""
            Questa vista analizza l'efficienza nell'uso delle risorse. I valori stimati sono confrontati con un benchmark ottimale (linea nera).
            - **Consumo Acqua Stimato**: **{consumi_stimati['acqua']:.0f} l/m²** (Ottimale: {benchmark_ottimali['acqua']:.0f} l/m²).
            - **Consumo Fertilizzanti**: **{consumi_stimati['fertilizzanti']:.3f} kg/m²** (Ottimale: {benchmark_ottimali['fertilizzanti']:.3f} kg/m²).
            """
        style_risorse['display'] = 'block'  # Rendiamo visibile solo questo
        return no_update, fig, no_update, style_prod, style_risorse, style_fin, spiegazione

    elif active_tab == 'tab-finanziaria':
        fig = go.Figure()
        fig.update_layout(annotations=[{"text": "Sezione in sviluppo...", "showarrow": False}])
        spiegazione = "Questa sezione analizzerà la performance finanziaria."

        style_fin['display'] = 'block'  # Rendiamo visibile solo questo
        return no_update, no_update, fig, style_prod, style_risorse, style_fin, spiegazione

    return no_update, no_update, no_update, style_prod, style_risorse, style_fin, "Seleziona una tab."
