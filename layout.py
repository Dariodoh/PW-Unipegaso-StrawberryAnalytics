# file: layout.py

from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app  # Importa l'istanza 'app' per usare le risorse (es. logo)


# --- Funzione Helper per creare i dropdown in modo pulito ---
def create_dropdown(title, control_id, options, default_value, info_button_id=None):
    """
    Crea un label (con un pulsante info opzionale) e un dropdown.
    """
    # Il titolo ora può contenere più elementi (label + bottone)
    label_content = [html.Label(f"{title}:")]
    if info_button_id:
        # Se viene fornito un ID, aggiungiamo un piccolo pulsante 'i'
        label_content.append(
            dbc.Button(
                "info", id=info_button_id, size="sm", color="info",
                className="rounded-circle ms-2 info-button-custom", n_clicks=0,
            )
        )

    return dbc.Col(
        html.Div([
            html.Div(label_content, className="d-flex align-items-center mb-2"),
            dcc.Dropdown(
                id=control_id,
                options=options,
                value=default_value,
                clearable=False
            )
        ]),
        width=4
    )

# --- Definiamo qui le opzioni per i dropdown ---
OPTIONS_TEMPERATURA = [
    {'label': '18-24°C', 'value': 'ottimale'},
    {'label': '12-17°C', 'value': 'sub-freddo'},
    {'label': '25-29°C', 'value': 'sub-caldo'},
    {'label': '<12°C', 'value': 'critico-freddo'},
    {'label': '>29°C', 'value': 'critico-caldo'},
]
OPTIONS_LUCE = [
    {'label': '> 12 ore/giorno', 'value': 'alta'},
    {'label': '8-12 ore/giorno', 'value': 'media'},
    {'label': '< 8 ore/giorno', 'value': 'bassa'},
]
OPTIONS_IRRIGAZIONE = [
    {'label': 'Goccia a goccia / Microirrigazione', 'value': 'goccia'},
    {'label': 'Aspersione', 'value': 'aspersione'},
    {'label': 'Manuale / Altro', 'value': 'manuale'},
]
OPTIONS_FERTILIZZAZIONE = [
    {'label': 'Soluzione Nutritiva Controllata', 'value': 'idroponica'},
    {'label': 'Fertirrigazione Bilanciata', 'value': 'fertirrigazione'},
    {'label': 'Organica (Letame/Compost)', 'value': 'organica'},
]
OPTIONS_PATOGENI = [
    {'label': 'Lotta Integrata', 'value': 'integrata'},
    {'label': 'Biologico (Prodotti naturali)', 'value': 'biologico'},
    {'label': 'Convenzionale (Prodotti di sintesi)', 'value': 'convenzionale'},
]
OPTIONS_RACCOLTA = [
    {'label': 'Ogni 1-2 giorni', 'value': 'alta'},
    {'label': 'Ogni 3-4 giorni', 'value': 'media'},
    {'label': 'Settimanale o più', 'value': 'bassa'},
]
OPTIONS_IMPOLLINAZIONE = [
    {'label': 'Con Bombi', 'value': 'bombi'},
    {'label': 'Naturale (Insetti autoctoni)', 'value': 'naturale'},
    {'label': 'Manuale / Assente', 'value': 'manuale'},
]
OPTIONS_DENSITA = [
    {'label': '> 7 piante/m²', 'value': 'alta'},
    {'label': '5-7 piante/m²', 'value': 'media'},
    {'label': '< 5 piante/m²', 'value': 'bassa'},
]
OPTIONS_UMIDITA = [
    {'label': '60-75%', 'value': 'ottimale'},
    {'label': '> 75%', 'value': 'alta_rischiosa'},
    {'label': '< 60%', 'value': 'bassa_stress'},
]

# --- Definizione del Layout Principale ---
layout = dbc.Container([
    # ... (header, card e la prima riga di dropdown rimangono invariati) ...
    dbc.Row([
        dbc.Col(
            html.Img(src=app.get_asset_url('logo.jpg'), height="300px"),
            width=12,
            className="mb-4 mt-4 d-flex justify-content-center"
        )
    ]),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                create_dropdown("Temperatura", "dd-temperatura", OPTIONS_TEMPERATURA, 'ottimale'),
                create_dropdown("Luce", "dd-luce", OPTIONS_LUCE, 'media'),
                create_dropdown("Irrigazione", "dd-irrigazione", OPTIONS_IRRIGAZIONE, 'goccia'),
            ], className="mb-3"),
            dbc.Row([
                create_dropdown("Umidità Relativa", "dd-umidita", OPTIONS_UMIDITA, 'ottimale'),
                create_dropdown("Fertilizzazione", "dd-fertilizzazione", OPTIONS_FERTILIZZAZIONE, 'fertirrigazione'),
                create_dropdown("Controllo Patogeni", "dd-patogeni", OPTIONS_PATOGENI, 'integrata'),
            ], className="mb-3"),
            dbc.Row([
                create_dropdown(
                    "Impollinazione", "dd-impollinazione", OPTIONS_IMPOLLINAZIONE, 'bombi',
                    info_button_id="btn-info-impollinazione"
                ),
                create_dropdown("Densità Coltivazione", "dd-densita", OPTIONS_DENSITA, 'media'),
                create_dropdown("Frequenza Raccolta", "dd-frequenza-raccolta", OPTIONS_RACCOLTA, 'media'),
            ])
        ]),
        className="mb-4 dropdown-panel-card"
    ),

    dbc.Row([
        # Colonna per il primo gruppo di preset
        dbc.Col([
            html.H4("Preset per tipo di coltura"),
            dbc.ButtonGroup([
                dbc.Button("Tradizionale", id="btn-preset-tradizionale", n_clicks=0, className="custom-button-green"),
                dbc.Button("Soilless", id="btn-preset-soilless", n_clicks=0, className="custom-button-green"),
                dbc.Button("Idroponica", id="btn-preset-idroponica", n_clicks=0, className="custom-button-green"),
            ])
        ], width=5),

        # Colonna per il secondo gruppo di preset
        dbc.Col([
            html.H4("Preset per condizioni"),
            dbc.ButtonGroup([
                dbc.Button("Sfavorevoli", id="btn-preset-sfavorevoli", n_clicks=0, className="custom-button-green"),
                dbc.Button("Medie", id="btn-preset-medie", n_clicks=0, className="custom-button-green"),
                dbc.Button("Ottimali", id="btn-preset-ottimali", n_clicks=0, className="custom-button-green"),
            ])
        ], width=5),

        # Colonna per il pulsante singolo
        dbc.Col([
            dbc.Button("Distribuzione Mensile", id="btn-distribuzione-mensile", n_clicks=0,
                       className="custom-button-green")
        ], width=2)

    ],
        align="end",
        className="mb-4"
    ),

    html.Hr(),


    dcc.Tabs(id="tabs-viste-grafici", value='tab-produttivo', children=[
        dcc.Tab(label='Andamento Produttivo', value='tab-produttivo'),
        dcc.Tab(label='Uso delle Risorse', value='tab-risorse'),
        dcc.Tab(label='Performance Finanziaria', value='tab-finanziaria'),
    ]),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                # Colonna sinistra per la spiegazione
                dbc.Col([
                    html.H4("Spiegazione del Grafico", id="titolo-spiegazione", className="text-white"),
                    html.Hr(className="border-white"),
                    dcc.Markdown(id="testo-spiegazione",
                                 children="*Seleziona una vista o modifica i parametri per visualizzare l'analisi...*")
                ], width=3, className="explanation-column"),  # Aggiungiamo una classe per il separatore

                # Colonna destra per il grafico
                dbc.Col([
                    dcc.Graph(id='grafico-principale', style={'height': '50vh'})
                ], width=9)
            ])
        ]),
        className="main-content-card"
    ),

    # Modale per la tabella mensile (esistente)
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Distribuzione Mensile della Produzione")),
        dbc.ModalBody(id="contenuto-tabella-mensile"),
        dbc.ModalFooter(dbc.Button("Chiudi", id="btn-chiudi-modale", className="ms-auto", n_clicks=0)),
    ], id="modale-tabella-mensile", size="xl", is_open=False),

    # --- NUOVO MODALE PER L'INFO IMPOLLINAZIONE ---
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Info: Impollinazione Controllata con Bombi")),
        dbc.ModalBody(id="contenuto-info-impollinazione"),  # Corpo con ID univoco
        dbc.ModalFooter(dbc.Button("Chiudi", id="btn-chiudi-modal-impollinazione", n_clicks=0)),
    ],
        id="modal-info-impollinazione",  # ID univoco per il modale
        size="xl",
        is_open=False,
    ),

], fluid=True)