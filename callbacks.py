# file: callbacks.py

from dash import Input, Output, State, callback_context, dcc, html, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data import prepare_benchmark_dataframe, simula_consumo_risorse, simula_performance_finanziaria, PESI_FATTORI

# Importiamo le risorse necessarie
from app import app
from data import get_calendario_colturale_fragola

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

        # Aggiorniamo la visibilità (stile)
        Output('container-produttivo', 'style'),
        Output('container-risorse', 'style'),
        Output('container-finanziario', 'style'),
        # Aggiorniamo la spiegazione
        Output('testo-spiegazione', 'children')
    ],
    [
        Input('tabs-viste-grafici', 'value'),
        *[Input(id, 'value') for id in PESI_FATTORI.keys()]
    ]
)
def update_main_view(active_tab, *valori_dropdown):
    fattori = dict(zip(PESI_FATTORI.keys(), valori_dropdown))

    df_plot, produzione_simulata = prepare_benchmark_dataframe(fattori)
    consumi_stimati, benchmark_ottimali = simula_consumo_risorse(fattori)
    dati_finanziari = simula_performance_finanziaria(produzione_simulata, consumi_stimati)

    # Stili di default per i contenitori: tutti nascosti
    style_hidden = {'display': 'none'}
    style_visible = {'display': 'block', 'width': '100%'}

    fig_produttivo = px.bar(
        df_plot, x='Produzione (kg/m²)', y='Scenario', orientation='h',
        title='Confronto Produzione Annua Stimata (kg/m²)', text_auto='.2f', color='Scenario',
        color_discrete_map={'Produzione Stimata': '#d13045', 'Produzione Media': '#7eb671',
                            'Produzione Ottimale': '#495b52', 'Produzione Sfavorevole': '#f0ad4e'}
    )
    fig_produttivo.update_layout(xaxis_title='Produzione (kg/m²)', yaxis_title=None, showlegend=False,
                                 plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#495b52'),
                                 title_x=0.5, title_xanchor='center')
    fig_produttivo.update_traces(textposition='outside',
                                 hovertemplate='<b>%{y}</b><br>Produzione: %{x:.2f} kg/m²<extra></extra>')

    fig_risorse = make_subplots(rows=1, cols=2, specs=[[{'type': 'indicator'}, {'type': 'indicator'}]],
                                subplot_titles=('Acqua (l/m²)', 'Fertilizzanti (kg/m²)'))
    fig_risorse.add_trace(go.Indicator(mode="gauge+number", value=consumi_stimati['acqua'],
                                       gauge={'axis': {'range': [None, 1250]}, 'bar': {'color': "#d13045"},
                                              'steps': [{'range': [0, 550], 'color': "#7eb671"},
                                                        {'range': [550, 750], 'color': "gold"}],
                                              'threshold': {'value': 500}}), row=1, col=1)
    fig_risorse.add_trace(
        go.Indicator(mode="gauge+number", value=consumi_stimati['fertilizzanti'], number={'valueformat': '.3f'},
                     gauge={'axis': {'range': [None, 0.175]}, 'bar': {'color': "#d13045"},
                            'steps': [{'range': [0, 0.077], 'color': "#7eb671"},
                                      {'range': [0.077, 0.105], 'color': "gold"}], 'threshold': {'value': 0.07}}),
        row=1, col=2)
    fig_risorse.update_layout(title_text="Stima del Consumo di Risorse vs. Ottimale", plot_bgcolor='rgba(0,0,0,0)',
                              paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#495b52'), title_x=0.5,
                              title_xanchor='center')

    ricavi_val = dati_finanziari['Ricavi (€/m²)']
    profitto_val = dati_finanziari['Profitto Lordo (€/m²)']
    costi_totali_val = ricavi_val - profitto_val

    fig_sankey = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5),
                                                     label=["Ricavi", "Costi Totali", "Profitto Lordo"],
                                                     color=["#495b52", "#d13045", "#7eb671"]),
                                           link=dict(source=[0, 0], target=[1, 2],
                                                     value=[costi_totali_val, profitto_val]),
                                           node_hovertemplate='<b>%{label}</b><br>Valore: €%{value:.2f}<extra></extra>')])
    fig_sankey.update_layout(title_text="Flusso Finanziario (€/m²)", font=dict(size=12, color='#495b52'),
                             plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                             margin=dict(t=40, b=20, l=10, r=10))

    costi_labels = ['Costo Acqua', 'Costo Fertilizzanti', 'Altri Costi']
    costi_values = [abs(dati_finanziari[k]) for k in costi_labels]
    color_map = {'Costo Acqua': '#7eb671','Costo Fertilizzanti': '#f0ad4e','Altri Costi': '#495b52'}
    final_colors = [color_map[label] for label in costi_labels]

    fig_ciambella = go.Figure(data=[
        go.Pie(labels=costi_labels, values=costi_values, hole=0.4, marker=dict(colors=final_colors),
               textposition='inside', textinfo='percent+label', hovertemplate='Costo: € %{value:.2f}<extra></extra>')])
    fig_ciambella.update_layout(title="Composizione dei Costi Variabili", showlegend=False,
                                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#495b52'),
                                title_x=0.5, title_xanchor='center', margin=dict(t=40, b=20, l=10, r=10))

    if active_tab == 'tab-produttivo':
        spiegazione = f"""
        Basandosi sui parametri di coltivazione selezionati, la produzione annua stimata è di **{produzione_simulata:.2f} kg/m²**.
    
        Questo valore si confronta con i seguenti benchmark standard per il settore:
        - **Produzione Ottimale**: 8.50 kg/m² (tipica di impianti ad alta tecnologia).
        - **Produzione Media**: 5.50 kg/m² (risultato comune per aziende ben gestite).
        - **Produzione Sfavorevole**: 3.00 kg/m² (in condizioni di stress o gestione non ideale).
    
        *Nota: questa è una simulazione basata su un modello. I risultati reali possono variare.*
        """

        return (fig_produttivo, fig_risorse, fig_sankey, fig_ciambella,
                style_visible, style_hidden, style_hidden, spiegazione)

        # --- TAB: USO DELLE RISORSE ---
    elif active_tab == 'tab-risorse':
        spiegazione = f"""
            Questa vista analizza l'efficienza nell'uso delle risorse. I valori stimati sono confrontati con un benchmark ottimale (linea nera).
            - **Consumo Acqua Stimato**: **{consumi_stimati['acqua']:.0f} l/m²** (Ottimale: {benchmark_ottimali['acqua']:.0f} l/m²).
            - **Consumo Fertilizzanti**: **{consumi_stimati['fertilizzanti']:.3f} kg/m²** (Ottimale: {benchmark_ottimali['fertilizzanti']:.3f} kg/m²).
            """

        return (fig_produttivo, fig_risorse, fig_sankey, fig_ciambella,
                style_hidden, style_visible, style_hidden, spiegazione)

    elif active_tab == 'tab-finanziaria':
        spiegazione = f"""
                Questa vista offre un'analisi finanziaria dettagliata per metro quadro (€/m²).

                **A sinistra**, il **diagramma di Sankey** mostra il flusso economico complessivo:
                - I **Ricavi** si suddividono in **Costi Totali** e nel **Profitto Lordo** finale.

                **A destra**, il **grafico a ciambella** analizza la composizione dei costi variabili, mostrando il peso percentuale di ogni voce.

                - **Ricavi Stimati**: **{ricavi_val:.2f} €/m²**
                - **Profitto Lordo Stimato**: **{profitto_val:.2f} €/m²**
                """
        return (fig_produttivo, fig_risorse, fig_sankey, fig_ciambella,
                style_hidden, style_hidden, style_visible, spiegazione)

        # Fallback
    return ([no_update] * 8)