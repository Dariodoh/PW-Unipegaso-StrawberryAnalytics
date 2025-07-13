from dash import Input, Output, State, callback_context, dcc, html, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

from app import app
from data import (
    get_calendario_colturale_fragola,
    prepare_benchmark_dataframe,
    simula_consumo_risorse,
    simula_performance_finanziaria
)

# Dizionario dei PRESETS per modificare simultaneamente i fattori
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

# Chiamata al modale per la costruzione della tabella Distribuzione Mensile
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


# Chiamata di apertura/chiusura al modale per la costruzione delle INFO su Impollinazione
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


# Chiamata di apertura/chiusura al modale per la costruzione delle INFO su Controllo Patogeni
@app.callback(
    Output("modal-info-patogeni", "is_open"),
    Output("contenuto-info-patogeni", "children"),
    Input("btn-info-patogeni", "n_clicks"),
    Input("btn-chiudi-modal-patogeni", "n_clicks"),
    State("modal-info-patogeni", "is_open"),
    prevent_initial_call=True
)
def toggle_patogeni_info_modal(n_open, n_close, is_open):
    ctx = callback_context
    if not ctx.triggered_id: raise PreventUpdate
    button_id = ctx.triggered_id
    if button_id == "btn-info-patogeni":
        testo_informativo = """
        La gestione delle malattie e dei parassiti è cruciale per la fragolicoltura. Le principali strategie si differenziano per approccio e impatto ambientale.

        #### Lotta Integrata
        È l'approccio più moderno ed equilibrato, promosso a livello europeo. Non mira a eliminare completamente i patogeni, ma a mantenerli sotto una soglia di danno economico. Si basa su:
        *   **Monitoraggio costante** delle colture per intervenire solo quando necessario.
        *   **Utilizzo prioritario di metodi naturali**: insetti utili (antagonisti), trappole, pratiche agronomiche preventive.
        *   **Interventi chimici mirati**: si ricorre a fitofarmaci solo come ultima risorsa, scegliendo prodotti a basso impatto ambientale e selettivi, per preservare gli organismi utili.
        
        È la strategia che garantisce il miglior compromesso tra efficacia, sostenibilità economica e rispetto per l'ambiente.

        ---

        #### Lotta Biologica
        Prevede l'uso **esclusivo** di organismi viventi (predatori, parassitoidi), microrganismi (funghi, batteri) o sostanze di origine naturale per controllare i patogeni. **Vieta completamente l'uso di fitofarmaci di sintesi**. Sebbene sia la scelta più ecologica, può risultare meno efficace in caso di forti infestazioni.

        #### Lotta Convenzionale (o a Calendario)
        È l'approccio tradizionale, basato su trattamenti con fitofarmaci di sintesi eseguiti a scadenze fisse ("a calendario"), indipendentemente dalla reale presenza del patogeno. Pur essendo efficace nel breve termine, presenta maggiori rischi di inquinamento, sviluppo di resistenze nei patogeni e danni agli insetti impollinatori.
        """
        contenuto = dcc.Markdown(testo_informativo, style={'textAlign': 'justify'})
        return True, contenuto
    if button_id == "btn-chiudi-modal-patogeni": return False, no_update
    return is_open, no_update


# Chiamata di apertura/chiusura al modale per la costruzione delle INFO su Tipologia di Coltura
@app.callback(
    Output("modal-info-coltura", "is_open"),
    Output("contenuto-info-coltura", "children"),
    Input("btn-info-coltura", "n_clicks"),
    Input("btn-chiudi-modal-coltura", "n_clicks"),
    State("modal-info-coltura", "is_open"),
    prevent_initial_call=True
)
def toggle_coltura_info_modal(n_open, n_close, is_open):
    ctx = callback_context
    if not ctx.triggered_id: raise PreventUpdate
    button_id = ctx.triggered_id
    if button_id == "btn-info-coltura":
        testo_informativo = """
        Il sistema di coltura definisce l'ambiente in cui le radici della pianta si sviluppano e assorbono nutrienti, influenzando drasticamente l'efficienza e la produttività.

        #### Suolo Tradizionale
        Le piante vengono coltivate direttamente nel terreno agricolo, in campo aperto o in serre. È il metodo più classico e diffuso.
        *   **Punti di Forza**: Bassi costi iniziali di impianto, minore complessità tecnologica.
        *   **Punti di Debolezza**: Maggiore consumo di acqua e fertilizzanti (dovuto a perdite per percolazione ed evaporazione), difficoltà nel controllare patogeni del suolo (stanchezza del terreno), produzione soggetta alle condizioni pedoclimatiche.

        ---

        #### Fuori Suolo (Soilless)
        Le piante crescono in contenitori (vasi, sacchi) riempiti con un substrato inerte (es. fibra di cocco, perlite, torba) anziché nel terreno. L'irrigazione e la nutrizione sono fornite tramite fertirrigazione a goccia.
        *   **Punti di Forza**: Eliminazione dei problemi legati ai patogeni del suolo, controllo preciso della nutrizione, maggiore efficienza nell'uso delle risorse rispetto al suolo, produzioni più uniformi e anticipate.
        *   **Punti di Debolezza**: Costo più elevato dell'impianto, necessità di gestire il drenaggio della soluzione nutritiva in eccesso (ciclo aperto).

        ---

        #### Idroponico a Ricircolo (Ciclo Chiuso)
        È la forma più avanzata di fuori suolo. Le radici sono immerse direttamente in una soluzione nutritiva liquida o in un film d'acqua che scorre in canali. Non c'è substrato solido o è minimo.
        *   **Punti di Forza**: **Massima efficienza** nell'uso di acqua e fertilizzanti (rispettivo risparmio fino al 90% e 60%), grazie al recupero e riutilizzo della soluzione nutritiva. Controllo totale dell'ambiente radicale, densità di impianto più elevate e produzioni potenzialmente maggiori.
        *   **Punti di Debolezza**: **Costi di impianto molto elevati**, alta dipendenza dalla tecnologia (pompe, sensori, sistemi di controllo), rischio di rapida diffusione di malattie radicali in tutto il sistema in caso di contaminazione.
        """
        contenuto = dcc.Markdown(testo_informativo, style={'textAlign': 'justify'})
        return True, contenuto
    if button_id == "btn-chiudi-modal-coltura": return False, no_update
    return is_open, no_update


# Chiamata di aggiornamento valori dei dropdown dai PRESETS
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


# Chiamata di aggiornamento tab per commento grafico dinamico e plot grafici
@app.callback(
    [
        Output('grafico-produttivo', 'figure'),
        Output('grafico-risorse', 'figure'),
        Output('grafico-sankey-finanziario', 'figure'),
        Output('grafico-composizione-costi', 'figure'),

        Output('container-produttivo', 'style'),
        Output('container-risorse', 'style'),
        Output('container-finanziario', 'style'),
        Output('testo-commentary', 'children')
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
    # Previene l'aggiornamento se i dropdown non sono ancora stati caricati
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

    # Gestione degli input per Performance Finanziaria, con fallback a 0 se non validi
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

    dati_finanziari = simula_performance_finanziaria(produzione_simulata, consumi_stimati, prezzo_vendita_val,
                                                     costo_acqua_val, costo_fert_val, costi_extra_val)

    # Commento dinamico e plot del grafico del tab Andamento Produttivo
    if active_tab == 'tab-produttivo':
        commentary = f"""
    Questa sezione analizza i parametri selezionati al fine di determinare una stima di produzione annuale.
    Basandosi sui suddetti parametri, la produzione annua stimata è di **{produzione_simulata:.2f} kg/m²**.

    Il grafico confronta questo risultato con i benchmark di riferimento:
    *   **Produzione Ottimale**: 8.50 kg/m²
    *   **Produzione Media**: 5.50 kg/m²
    *   **Produzione Sfavorevole**: 3.00 kg/m²

    La resa produttiva è il risultato diretto delle scelte effettuate. Si noti che il **Sistema di Coltura** è uno dei fattori più determinanti. 
    
    Mentre i sistemi tradizionali tendono ad allinearsi con fatica a questi benchmark, le tecnologie avanzate come il **Fuori Suolo** e soprattutto l'**Idroponica a Ricircolo** hanno il potenziale per superarli ampiamente. Questo perché permettono un controllo capillare dell'ambiente di crescita, massimizzando l'efficienza della pianta.

    Utilizzando i **PRESET PER TIPO DI COLTURA** si può osservare direttamente questa dinamica e vedere come una gestione ottimale possa portare a risultati produttivi al di sopra dei **10 kg/m²**.

    *Nota: questa è una stima basata su un modello simulativo.*
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

        return fig_produttivo, no_update, no_update, no_update, style_visible, style_hidden, style_hidden, commentary

    # Commento dinamico e plot dei grafici del tab Uso delle Risorse
    elif active_tab == 'tab-risorse':
        commentary = f"""
            Questa sezione analizza l'efficienza nell'uso delle risorse idriche e nutritive, fondamentali per una produzione di qualità.

            #### Utilizzo dell'Acqua
            Il consumo stimato è di **{consumi_stimati['acqua']:.0f} l/m²**. Il range ottimale è 300-450 l/m². Condizioni sfavorevoli possono indicare:
            *   **Carenza (< 300 l/m²)**: indica uno stress idrico che compromette la crescita della pianta e la pezzatura (dimensione) dei frutti.
            *   **Spreco (> 650 l/m²)**: rappresenta un impatto economico e ambientale considerevole. Può creare condizioni di asfissia per le radici e favorire lo sviluppo di malattie fungine.

            #### Utilizzo dei Fertilizzanti
            Il consumo stimato è di **{consumi_stimati['fertilizzanti']:.3f} kg/m²**. Questo valore rappresenta il consumo totale di elementi, calcolato sui fabbisogni principali della fragola: **Azoto (N)**, **Fosforo (P₂O₅)** e **Potassio (K₂O)**. Condizioni sfavorevoli possono indicare:
            *   **Carenza (< 0.01 kg/m²)**: limita fortemente lo sviluppo vegetativo, la fioritura e l'ingrossamento dei frutti, riducendo la qualità del raccolto.
            *   **Eccesso (> 0.02 kg/m²)**: oltre a essere un costo superfluo, può causare squilibri nutrizionali, eccessiva vegetazione a scapito dei frutti e potenziale inquinamento delle falde.
            
            In un sistema **Idroponico a Ricircolo**, i benchmark tradizionali vengono rivoluzionati: l'efficienza è massima perché acqua e nutrienti vengono recuperati e riutilizzati.
            
            **In questo scenario, un basso consumo non indica carenza, ma concreta efficienza.**

            *   **Acqua**: minore sarà il valore, più il risultato sarà considerato eccellente, riflettendo un risparmio idrico che può arrivare fino al 90% rispetto alla coltura in suolo. Lo spreco è quasi nullo.
            *   **Fertilizzanti**: allo stesso modo, il basso consumo è indice di una gestione ottimale, in ogni grammo di nutriente viene reso disponibile alla pianta, limitando la dispersione/spreco e garantendo un risparmio fino al 60% rispetto alla coltura in suolo. 
            
            I grafici mostrano come questa tecnologia ridefinisca il concetto di "ottimale".
            
            *Nota: questa è una stima basata su un modello simulativo.*
            """

        fig_risorse = make_subplots(rows=1, cols=2, specs=[[{'type': 'indicator'}, {'type': 'indicator'}]],
                                    subplot_titles=('Acqua (l/m²)', 'Fertilizzanti (kg/m²)'))

        # Discrimine dei range sfavorevoli/medi/ottimali per coltura di tipo idroponica
        if fattori_agronomici['dd-sistema-colturale'] == 'idroponico_ricircolo':
            gauge_acqua_steps = [{'range': [0, 100], 'color': "#7eb671"},
                                 {'range': [100, 200], 'color': "gold"},
                                 {'range': [200, 1000], 'color': "#d13045"}]
            gauge_acqua_range = [0, 250]
            acqua_threshold_value = 50

            # Gauge Fertilizzanti per Idroponica
            gauge_fert_steps = [{'range': [0, 0.008], 'color': "#7eb671"},
                                {'range': [0.008, 0.015], 'color': "gold"},
                                {'range': [0.015, 0.035], 'color': "#d13045"}]
            gauge_fert_range = [0, 0.02]
            fert_threshold_value = 0.004

        # Discrimine dei range sfavorevoli/medi/ottimali per coltura di altro tipo
        else:
            gauge_acqua_steps = [{'range': [0, 300], 'color': "#d13045"},
                                 {'range': [300, 450], 'color': "#7eb671"},
                                 {'range': [450, 650], 'color': "gold"},
                                 {'range': [650, 1000], 'color': "#d13045"}]
            gauge_acqua_range = [0, 1000]
            acqua_threshold_value = 375

            gauge_fert_steps = [{'range': [0, 0.010], 'color': "#d13045"},
                                {'range': [0.010, 0.015], 'color': "#7eb671"},
                                {'range': [0.015, 0.020], 'color': "gold"},
                                {'range': [0.020, 0.030], 'color': "#d13045"}]
            gauge_fert_range = [0, 0.030]
            fert_threshold_value = 0.0125

        fig_risorse.add_trace(go.Indicator(mode="gauge+number", value=consumo_acqua_simulato, uid='gauge-acqua-background-uid',
                                           gauge={'shape': "angular",
                                               'axis': {'range': gauge_acqua_range},
                                                  'steps': gauge_acqua_steps,
                                                  }), row=1, col=1)
        fig_risorse.add_trace(go.Indicator(mode="gauge", value=consumo_acqua_simulato, uid='gauge-acqua-bar-uid',
                                           gauge={'shape': "angular",
                                               'axis': {'range': gauge_acqua_range}, 'bar': {'color': "#495b52"},
                                                  'threshold': {'value': acqua_threshold_value}
                                                  }), row=1, col=1)
        fig_risorse.add_trace(
            go.Indicator(mode="gauge+number", value=consumo_fertilizzanti_simulato, uid='gauge-fert-background-uid',
                         number={'valueformat': '.3f'},
                         gauge={'shape': "angular",
                             'axis': {'range': gauge_fert_range},
                                'steps': gauge_fert_steps,
                                }), row=1, col=2)
        fig_risorse.add_trace(
            go.Indicator(mode="gauge", value=consumo_fertilizzanti_simulato, uid='gauge-fert-bar-uid',
                         #number={'valueformat': '.3f'},
                         gauge={'shape': "angular",
                             'axis': {'range': gauge_fert_range}, 'bar': {'color': "#495b52"},
                                #'steps': gauge_fert_steps,
                                'threshold': {'value': fert_threshold_value}
                                }), row=1, col=2)

        fig_risorse.update_layout(title_text="Stima del Consumo di Risorse", plot_bgcolor='rgba(0,0,0,0)',
                                  paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#495b52'), title_x=0.5,
                                  title_xanchor='center', transition_duration=500)

        return no_update, fig_risorse, no_update, no_update, style_hidden, style_visible, style_hidden, commentary

    # Commento dinamico e plot dei grafici del tab Performance Finanziaria
    elif active_tab == 'tab-finanziaria':

        ricavi_val = dati_finanziari['Ricavi (€/m²)']
        profitto_val = dati_finanziari['Profitto Lordo (€/m²)']
        costi_totali_val = ricavi_val - profitto_val

        commentary = f"""
        Questa sezione analizza la sostenibilità economica della coltivazione, mostrando come le scelte agronomiche e i parametri di mercato si traducono in profitto.

        **Interazione e Analisi "What-if":**
        questa è la sezione più sensibile alle fluttuazioni di mercato. Modificando i **parametri economici** (soprattutto il **prezzo di vendita**) si può osservare come un piccolo cambiamento possa avere un impatto enorme sul profitto. Ad esempio, una produzione alta ad un prezzo di vendita basso potrebbe risultare meno redditizia di una produzione media venduta ad un prezzo più alto.

        **Grafico di Flusso (Sankey)** a sinistra:
        illustra il percorso economico complessivo. I **Ricavi Totali ({ricavi_val:.2f} €/m²)**, generati dalla vendita della produzione, si dividono in due flussi: i **Costi Totali ({costi_totali_val:.2f} €/m²)** sostenuti e il **Profitto Lordo ({profitto_val:.2f} €/m²)** finale. Questo grafico evidenzia immediatamente la proporzione tra costi e ricavi.

        **Grafico a Ciambella** a destra:
        offre uno spaccato dettagliato dei **costi variabili**. Mostra il peso percentuale di ogni voce, consentendo di comprendere quali fattori incidono maggiormente sulle spese.

        **Cosa si intende per "Altri Costi Variabili":**
        questa macro-categoria include tutte le spese operative non legate direttamente ad acqua e fertilizzanti, come ad esempio:
        *   Manodopera per trapianto, gestione e raccolta.
        *   Costo delle piante e del materiale di propagazione.
        *   Noleggio o acquisto di insetti impollinatori (bombi).
        *   Energia elettrica per pompe e sistemi di controllo.
        *   Materiali di consumo (es. substrati, teli per pacciamatura).
        
        *Nota: questa è una stima basata su un modello simulativo.*
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
                   textposition='inside', textinfo='percent+label',
                   hovertemplate='Costo: € %{value:.2f}<extra></extra>')])
        fig_ciambella.update_layout(title="Composizione dei Costi Variabili", showlegend=False,
                                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='#495b52'),
                                    title_x=0.5, title_xanchor='center', margin=dict(t=40, b=20, l=10, r=10))

        return no_update, no_update, fig_sankey, fig_ciambella, style_hidden, style_hidden, style_visible, commentary

    # Fallback per valore di active_tab diverso
    return [no_update] * 8
