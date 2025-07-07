# file: callbacks.py

from dash import Input, Output, State, callback_context, dcc, html, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Importiamo le risorse necessarie
from app import app
from data import (
    get_calendario_colturale_fragola,
    prepare_benchmark_dataframe,
    simula_consumo_risorse,
    simula_performance_finanziaria,
    IMPATTI_RISORSE
)

PRESETS = {
    "btn-preset-tradizionale": {
        'dd-temperatura': 'sub-freddo',
        'dd-luce': 'media',
        'dd-umidita': 'alta_rischiosa',
        'dd-irrigazione': 'manuale',
        'dd-fertilizzazione': 'organica',
        'dd-patogeni': 'convenzionale',
        'dd-frequenza-raccolta': 'bassa',
        'dd-impollinazione': 'naturale',
        'dd-sistema-colturale': 'suolo_tradizionale'
    },
    "btn-preset-soilless": {
        'dd-temperatura': 'ottimale',
        'dd-luce': 'alta',
        'dd-umidita': 'ottimale',
        'dd-irrigazione': 'goccia',
        'dd-fertilizzazione': 'fertirrigazione',
        'dd-patogeni': 'integrata',
        'dd-frequenza-raccolta': 'media',
        'dd-impollinazione': 'bombi',
        'dd-sistema-colturale': 'soilless_aperto'
    },
    "btn-preset-idroponica": {
        'dd-temperatura': 'ottimale',
        'dd-luce': 'alta',
        'dd-umidita': 'ottimale',
        'dd-irrigazione': 'goccia',
        'dd-fertilizzazione': 'idroponica',
        'dd-patogeni': 'integrata',
        'dd-frequenza-raccolta': 'alta',
        'dd-impollinazione': 'bombi',
        'dd-sistema-colturale': 'idroponico_ricircolo'
    },
    "btn-preset-sfavorevoli": {
        'dd-temperatura': 'critico', 'dd-luce': 'bassa', 'dd-umidita': 'alta_rischiosa', 'dd-irrigazione': 'manuale',
        'dd-fertilizzazione': 'organica', 'dd-patogeni': 'convenzionale', 'dd-frequenza-raccolta': 'bassa',
        'dd-impollinazione': 'manuale', 'dd-sistema-colturale': 'suolo_tradizionale'
    },
    "btn-preset-medie": {
        'dd-temperatura': 'sub-caldo', 'dd-luce': 'media', 'dd-umidita': 'alta_rischiosa',
        'dd-irrigazione': 'aspersione',
        'dd-fertilizzazione': 'fertirrigazione', 'dd-patogeni': 'biologico', 'dd-frequenza-raccolta': 'media',
        'dd-impollinazione': 'naturale', 'dd-sistema-colturale': 'soilless_aperto'
    },
    "btn-preset-ottimali": {
        'dd-temperatura': 'ottimale', 'dd-luce': 'alta', 'dd-umidita': 'ottimale', 'dd-irrigazione': 'goccia',
        'dd-fertilizzazione': 'idroponica', 'dd-patogeni': 'integrata', 'dd-frequenza-raccolta': 'alta',
        'dd-impollinazione': 'bombi', 'dd-sistema-colturale': 'idroponico_ricircolo'
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
    [
        Output("dd-temperatura", "value"),
        Output("dd-luce", "value"),
        Output("dd-umidita", "value"),
        Output("dd-irrigazione", "value"),
        Output("dd-fertilizzazione", "value"),
        Output("dd-patogeni", "value"),
        Output("dd-frequenza-raccolta", "value"),  # 7° posto
        Output("dd-impollinazione", "value"),  # 8° posto
        Output("dd-sistema-colturale", "value")
    ],
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
    button_id = ctx.triggered_id.split(".")[0]
    if button_id in PRESETS:
        preset_values = PRESETS[button_id]
        return list(preset_values.values())
    return [no_update] * 9


@app.callback(
    # Aggiorniamo le figure
    [
        Output('grafico-produttivo', 'figure'),
        Output('grafico-risorse', 'figure'),
        Output('grafico-sankey-finanziario', 'figure'),
        Output('grafico-composizione-costi', 'figure'),

        Output('container-produttivo', 'style'),
        Output('container-risorse', 'style'),
        Output('container-finanziario', 'style'),
        Output('testo-spiegazione', 'children')
    ],
    [
        Input('tabs-viste-grafici', 'value'),
        Input('dd-temperatura', 'value'),
        Input('dd-luce', 'value'),
        Input('dd-umidita', 'value'),
        Input('dd-irrigazione', 'value'),
        Input('dd-fertilizzazione', 'value'),
        Input('dd-patogeni', 'value'),
        Input('dd-frequenza-raccolta', 'value'),
        Input('dd-impollinazione', 'value'),
        Input('dd-sistema-colturale', 'value'),
        Input('input-prezzo-vendita', 'value'),
        Input('input-costo-acqua', 'value'),
        Input('input-costo-fertilizzanti', 'value'),
        Input('input-costi-extra', 'value')
    ]
)
def update_main_view(active_tab,
                     temp, luce, umidita, irrigazione, fertilizzazione,
                     patogeni, raccolta, impollinazione, sistema,
                     prezzo_vendita, costo_acqua, costo_fert, costi_extra):

    # Prevenire l'aggiornamento se i dropdown non sono ancora stati caricati
    if not all([temp, luce, umidita, irrigazione, fertilizzazione, patogeni, raccolta, impollinazione, sistema]):
        raise PreventUpdate

    # Stili per la visibilità dei container
    style_hidden = {'display': 'none'}
    style_visible = {'display': 'block', 'width': '100%'}

    fattori_agronomici = {
        'dd-temperatura': temp, 'dd-luce': luce, 'dd-umidita': umidita,
        'dd-irrigazione': irrigazione, 'dd-fertilizzazione': fertilizzazione,
        'dd-patogeni': patogeni, 'dd-frequenza-raccolta': raccolta,
        'dd-impollinazione': impollinazione, 'dd-sistema-colturale': sistema
    }

    df_plot, produzione_simulata = prepare_benchmark_dataframe(fattori_agronomici)
    consumi_stimati = simula_consumo_risorse(fattori_agronomici)
    consumo_acqua_simulato = consumi_stimati['acqua']
    consumo_fertilizzanti_simulato = consumi_stimati['fertilizzanti']

    # Gestione robusta degli input economici, con fallback a 0 se non validi
    try:
        prezzo_vendita_val = float(prezzo_vendita)
    except (ValueError, TypeError):
        prezzo_vendita_val = 0
    try:
        costo_acqua_val = float(costo_acqua)
    except (ValueError, TypeError):
        costo_acqua_val = 0
    try:
        costo_fert_val = float(costo_fert)
    except (ValueError, TypeError):
        costo_fert_val = 0
    try:
        costi_extra_val = float(costi_extra)
    except (ValueError, TypeError):
        costi_extra_val = 0

    dati_finanziari = simula_performance_finanziaria(produzione_simulata, consumi_stimati, prezzo_vendita_val, costo_acqua_val, costo_fert_val, costi_extra_val)

    if active_tab == 'tab-produttivo':
        spiegazione = f"""
        Basandosi sui parametri di coltivazione selezionati, la produzione annua stimata è di **{produzione_simulata:.2f} kg/m²**.

        Questo valore si confronta con i seguenti benchmark standard per il settore:
        - **Produzione Ottimale**: 8.50 kg/m² (tipica di impianti ad alta tecnologia).
        - **Produzione Media**: 5.50 kg/m² (risultato comune per aziende ben gestite).
        - **Produzione Sfavorevole**: 3.00 kg/m² (in condizioni di stress o gestione non ideale).

        *Nota: questa è una simulazione basata su un modello. I risultati reali possono variare.*
        """

        fig_produttivo = px.bar(
            df_plot, x='Produzione (kg/m²)', y='Scenario', orientation='h',
            title='Confronto Produzione Annua Stimata (kg/m²)', text_auto='.2f', color='Scenario',
            color_discrete_map={'Produzione Stimata': '#495b52', 'Produzione Sfavorevole': '#d13045',
                                'Produzione Media': 'gold', 'Produzione Ottimale': '#7eb671'}
        )
        fig_produttivo.update_traces(uid='bar-prod-uid', textposition='outside',
                                     hovertemplate='<b>%{y}</b><br>Produzione: %{x:.2f} kg/m²<extra></extra>')
        fig_produttivo.update_layout(xaxis_title='Produzione (kg/m²)', yaxis_title=None, showlegend=False,
                                     plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                     font=dict(color='#495b52'),
                                     title_x=0.5, title_xanchor='center', transition_duration=500)

        max_range = max(produzione_simulata, 8.5) * 1.1
        fig_produttivo.update_xaxes(range=[0, max_range])

        return fig_produttivo, no_update, no_update, no_update, style_visible, style_hidden, style_hidden, spiegazione

    elif active_tab == 'tab-risorse':
        spiegazione = f"""
                    Questa vista analizza l'efficienza nell'uso delle risorse. I valori stimati sono confrontati con un benchmark ottimale (linea nera).
                    - **Consumo Acqua Stimato**: **{consumo_acqua_simulato:.0f} l/m²** (Ottimale: 300-450 l/m²).
                    - **Consumo Fertilizzanti**: **{consumo_fertilizzanti_simulato:.3f} kg/m²** (Ottimale: 0.010-0.015 kg/m²).
                    INSERIRE SPIEGAZIONE MODIFICA GRAFICO SE IDROPONICA
                    """

        fig_risorse = make_subplots(rows=1, cols=2, specs=[[{'type': 'indicator'}, {'type': 'indicator'}]],
                                    subplot_titles=('Acqua (l/m²)', 'Fertilizzanti (kg/m²)'))

        if fattori_agronomici['dd-sistema-colturale'] == 'idroponico_ricircolo':
            spiegazione = f"""... testo specifico per idroponica ..."""
            # Gauge Acqua per Idroponica: più basso è, meglio è.
            gauge_acqua_steps = [{'range': [0, 100], 'color': "#7eb671"},  # Ottimale
                                 {'range': [100, 200], 'color': "gold"},  # Spreco
                                 {'range': [200, 1000], 'color': "#d13045"}]  # Grave spreco
            gauge_acqua_range = [None, 250]

            # Gauge Fertilizzanti per Idroponica
            gauge_fert_steps = [{'range': [0, 0.008], 'color': "#7eb671"},  # Ottimale
                                {'range': [0.008, 0.015], 'color': "gold"},
                                {'range': [0.015, 0.035], 'color': "#d13045"}]
            gauge_fert_range = [None, 0.02]
        else:
            # Gauge standard per Suolo
            gauge_acqua_steps = [{'range': [0, 300], 'color': "#d13045"},
                                 {'range': [300, 450], 'color': "#7eb671"},
                                 {'range': [450, 650], 'color': "gold"},
                                 {'range': [650, 1000], 'color': "#d13045"}]
            gauge_acqua_range = [None, 1000]

            gauge_fert_steps = [{'range': [0, 0.010], 'color': "#d13045"},
                                {'range': [0.010, 0.015], 'color': "#7eb671"},
                                {'range': [0.015, 0.020], 'color': "gold"},
                                {'range': [0.020, 0.030], 'color': "#d13045"}]
            gauge_fert_range = [None, 0.030]


        fig_risorse.add_trace(go.Indicator(mode="gauge+number", value=consumo_acqua_simulato, uid='gauge-acqua-uid',
                                           gauge={'axis': {'range': gauge_acqua_range}, 'bar': {'color': "#495b52"},
                                                  'steps': gauge_acqua_steps,
                                                  'threshold': {'value': 375}}), row=1, col=1)
        fig_risorse.add_trace(
            go.Indicator(mode="gauge+number", value=consumo_fertilizzanti_simulato, uid='gauge-fert-uid',
                         number={'valueformat': '.3f'},
                         gauge={'axis': {'range': gauge_fert_range}, 'bar': {'color': "#495b52"},
                                'steps': gauge_fert_steps,
                                'threshold': {'value': 0.07}}),row=1, col=2)

        fig_risorse.update_layout(title_text="Stima del Consumo di Risorse vs. Ottimale", plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#495b52'), title_x=0.5,
                                  title_xanchor='center', transition_duration=500)

        return no_update, fig_risorse, no_update, no_update, style_hidden, style_visible, style_hidden, spiegazione

    elif active_tab == 'tab-finanziaria':

        ricavi_val = dati_finanziari['Ricavi (€/m²)']
        profitto_val = dati_finanziari['Profitto Lordo (€/m²)']
        costi_totali_val = ricavi_val - profitto_val

        spiegazione = f"""
            Questa vista offre un'analisi finanziaria dettagliata per metro quadro (€/m²).
    
            **A sinistra**, il **diagramma di Sankey** mostra il flusso economico complessivo:
            - I **Ricavi** si suddividono in **Costi Totali** e nel **Profitto Lordo** finale.
    
            **A destra**, il **grafico a ciambella** analizza la composizione dei costi variabili, mostrando il peso percentuale di ogni voce.
    
            - **Ricavi Stimati**: **{ricavi_val:.2f} €/m²**
            - **Profitto Lordo Stimato**: **{profitto_val:.2f} €/m²**
            """

        fig_sankey = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5),
                                                         label=["Ricavi", "Costi Totali", "Profitto Lordo"],
                                                         color=["#495b52", "#d13045", "#7eb671"]),
                                               uid='sankey-flow-uid',
                                               link=dict(source=[0, 0], target=[1, 2],
                                                         value=[costi_totali_val, profitto_val]),
                                               node_hovertemplate='<b>%{label}</b><br>Valore: €%{value:.2f}<extra></extra>')])
        fig_sankey.update_layout(title_text="Flusso Finanziario (€/m²)", font=dict(size=12, color='#495b52'),
                                 transition_duration=500,
                                 plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                 margin=dict(t=40, b=20, l=10, r=10))

        costi_labels = ['Costo Acqua', 'Costo Fertilizzanti', 'Altri Costi']
        costi_values = [abs(dati_finanziari[k]) for k in costi_labels]
        color_map = {'Costo Acqua': '#63cec7', 'Costo Fertilizzanti': '#7eb671', 'Altri Costi': 'gold'}
        final_colors = [color_map[label] for label in costi_labels]

        fig_ciambella = go.Figure(data=[
            go.Pie(labels=costi_labels, values=costi_values, hole=0.4, marker=dict(colors=final_colors),
                   # uid='pie-costs-uid',
                   textposition='inside', textinfo='percent+label',
                   hovertemplate='Costo: € %{value:.2f}<extra></extra>')])
        fig_ciambella.update_layout(title="Composizione dei Costi Variabili", showlegend=False,
                                    # transition_duration=500,
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='#495b52'),
                                    title_x=0.5, title_xanchor='center', margin=dict(t=40, b=20, l=10, r=10))

        return no_update, no_update, fig_sankey, fig_ciambella, style_hidden, style_hidden, style_visible, spiegazione

    # Fallback nel caso active_tab non corrisponda a nessuna opzione
    return [no_update] * 8