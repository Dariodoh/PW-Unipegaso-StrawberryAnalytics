# file: callbacks.py

from dash import Input, Output, State, callback_context, dcc, html, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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


# --- 1. Algoritmo di Simulazione ---
PRODUZIONE_BASE_OTTIMALE = 10.0  # kg/m², potenziale massimo teorico

# Dizionario dei pesi: associa ogni opzione a un range di moltiplicatori (min, max)
PESI_FATTORI = {
    'dd-temperatura': {'ottimale': (0.95, 1.0), 'sub-freddo': (0.7, 0.85), 'sub-caldo': (0.6, 0.75),
                       'critico': (0.2, 0.4)},
    'dd-luce': {'alta': (0.95, 1.0), 'media': (0.8, 0.9), 'bassa': (0.5, 0.7)},
    'dd-irrigazione': {'goccia': (0.98, 1.0), 'aspersione': (0.75, 0.85), 'manuale': (0.6, 0.7)},
    'dd-fertilizzazione': {'idroponica': (1.0, 1.0), 'fertirrigazione': (0.85, 0.95), 'organica': (0.65, 0.8)},
    'dd-patogeni': {'integrata': (0.9, 1.0), 'biologico': (0.75, 0.85), 'convenzionale': (0.8, 0.9)},
    'dd-frequenza-raccolta': {'alta': (0.95, 1.0), 'media': (0.8, 0.9), 'bassa': (0.6, 0.75)},
    'dd-impollinazione': {'bombi': (0.98, 1.0), 'naturale': (0.7, 0.85), 'manuale': (0.4, 0.6)},
    'dd-densita': {'alta': (0.9, 1.0), 'media': (0.8, 0.9), 'bassa': (0.6, 0.7)},
    'dd-umidita': {'ottimale': (0.95, 1.0), 'alta_rischiosa': (0.6, 0.8), 'bassa_stress': (0.7, 0.85)},
}


def simula_produzione_annua(fattori_selezionati):
    """
    Calcola la produzione annua simulata in kg/m² basandosi sui fattori selezionati.
    """
    produzione_corrente = PRODUZIONE_BASE_OTTIMALE

    for fattore_id, valore_selezionato in fattori_selezionati.items():
        # Trova il range di pesi per il valore selezionato di quel fattore
        range_peso = PESI_FATTORI[fattore_id][valore_selezionato]
        # Estrai un moltiplicatore casuale da quel range
        moltiplicatore = np.random.uniform(range_peso[0], range_peso[1])
        # Applica il moltiplicatore
        produzione_corrente *= moltiplicatore

    return produzione_corrente


# --- 2. Callback Principale per il Grafico ---
@app.callback(
    Output('grafico-principale', 'figure'),
    Output('testo-spiegazione', 'children'),
    # L'Input è la Tab attiva + tutti i 9 dropdown
    Input('tabs-viste-grafici', 'value'),
    *[Input(id, 'value') for id in PESI_FATTORI.keys()]
)
def update_main_graph(active_tab, *valori_dropdown):
    # Se la tab attiva non è 'Andamento Produttivo', non fare nulla per ora
    if active_tab != 'tab-produttivo':
        # Puoi restituire un grafico vuoto e un messaggio
        fig_vuota = go.Figure()
        fig_vuota.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {"text": "Seleziona un'altra vista per l'analisi", "xref": "paper", "yref": "paper", "showarrow": False,
                 "font": {"size": 20}}]
        )
        return fig_vuota, dcc.Markdown("Questa sezione mostra l'andamento produttivo. Seleziona le altre tab per diverse analisi.")

    # 1. Raccogli i valori dei dropdown in un dizionario
    fattori = dict(zip(PESI_FATTORI.keys(), valori_dropdown))

    # 2. Esegui la simulazione
    produzione_simulata = simula_produzione_annua(fattori)

    # 3. Definisci i benchmark
    benchmark = {
        'Sfavorevole': 3.0,  # kg/m²
        'Media': 5.5,  # kg/m²
        'Ottimale': 8.5,  # kg/m²
    }

    # 4. Prepara i dati per il grafico
    data_to_plot = {
        'Scenario': ['Scenario Scelto', 'Produzione Media', 'Produzione Ottimale', 'Produzione Sfavorevole'],
        'Produzione (kg/m²)': [produzione_simulata, benchmark['Media'], benchmark['Ottimale'], benchmark['Sfavorevole']]
    }
    df_plot = pd.DataFrame(data_to_plot)

    # 5. Crea il grafico a barre
    fig = px.bar(
        df_plot,
        x='Scenario',
        y='Produzione (kg/m²)',
        title='Confronto Produzione Annua Stimata (kg/m²)',
        text_auto='.2f',  # Mostra il valore sopra ogni barra, con 2 decimali
        color='Scenario',  # Colora ogni barra in modo diverso
        color_discrete_map={
            'Scenario Scelto': '#d13045',  # Il nostro colore rosso per evidenziare
            'Produzione Media': '#7eb671',
            'Produzione Ottimale': '#495b52',
            'Produzione Sfavorevole': '#f0ad4e'
        }
    )
    fig.update_layout(
        xaxis_title=None,
        yaxis_title='Produzione (kg/m²)',
        showlegend=False,  # La legenda è ridondante con le etichette dell'asse x
        plot_bgcolor='rgba(0,0,0,0)',  # Sfondo del plot trasparente
        paper_bgcolor='rgba(0,0,0,0)',  # Sfondo generale trasparente
        font=dict(color='#495b52')  # Colore del testo
    )
    fig.update_traces(textposition='outside')

    # 6. Crea la spiegazione dinamica
    spiegazione = f"""
    Basandosi sui parametri di coltivazione selezionati, la produzione annua stimata è di **{produzione_simulata:.2f} kg/m²**.

    Questo valore si confronta con i seguenti benchmark standard per il settore:
    - **Produzione Ottimale**: {benchmark['Ottimale']:.2f} kg/m² (tipica di impianti ad alta tecnologia).
    - **Produzione Media**: {benchmark['Media']:.2f} kg/m² (risultato comune per aziende ben gestite).
    - **Produzione Sfavorevole**: {benchmark['Sfavorevole']:.2f} kg/m² (in condizioni di stress o gestione non ideale).

    *Nota: questa è una simulazione basata su un modello. I risultati reali possono variare.*
    """

    return fig, dcc.Markdown(spiegazione)