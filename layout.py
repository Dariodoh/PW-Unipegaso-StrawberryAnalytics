# file: layout.py

from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app


# --- Funzione Helper per creare i dropdown in modo pulito ---
def create_dropdown(title, control_id, options, default_value, width, info_button_id=None):
    """
    Crea un label (con un pulsante info opzionale) e un dropdown.
    """
    # Il titolo ora può contenere più elementi (label + bottone)
    label_content = [html.Label(f"{title}:", className="form-label")]
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
        width=width
    )


# --- Definiamo qui le opzioni per i dropdown ---
OPTIONS_TEMPERATURA = [
    {'label': '18-24°C', 'value': 'ottimale'},
    {'label': '12-17°C', 'value': 'sub-freddo'},
    {'label': '25-29°C', 'value': 'sub-caldo'},
    {'label': '<12°C', 'value': 'critico'},
    {'label': '>29°C', 'value': 'critico'},
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
OPTIONS_UMIDITA = [
    {'label': '60-75%', 'value': 'ottimale'},
    {'label': '> 75%', 'value': 'alta_rischiosa'},
    {'label': '< 60%', 'value': 'bassa_stress'},
]
OPTIONS_SISTEMA = [
    {'label': 'In Suolo Tradizionale', 'value': 'suolo_tradizionale'},
    {'label': 'Fuori Suolo (Drenaggio a perdere)', 'value': 'soilless_aperto'},
    {'label': 'Idroponico (Ricircolo)', 'value': 'idroponico_ricircolo'},
]

# --- Definizione del Layout Principale ---
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('logo.jpg'), height="150px"), width=12,
                className="mb-4 mt-4 d-flex justify-content-center")
    ]),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                create_dropdown("Temperatura", "dd-temperatura", OPTIONS_TEMPERATURA, 'ottimale', width="2"),
                create_dropdown("Luce", "dd-luce", OPTIONS_LUCE, 'media', width="2"),
                create_dropdown("Umidità Relativa", "dd-umidita", OPTIONS_UMIDITA, 'ottimale', width="2"),
                create_dropdown("Fertilizzazione", "dd-fertilizzazione", OPTIONS_FERTILIZZAZIONE, 'fertirrigazione',
                                width="2"),
                create_dropdown("Frequenza Raccolta", "dd-frequenza-raccolta", OPTIONS_RACCOLTA, 'media', width="2"),
                create_dropdown("Impollinazione", "dd-impollinazione", OPTIONS_IMPOLLINAZIONE, 'bombi',
                                info_button_id="btn-info-impollinazione", width="2"),
            ], className="mb-3"),
            dbc.Row([
                create_dropdown("Irrigazione", "dd-irrigazione", OPTIONS_IRRIGAZIONE, 'goccia', width="4"),
                create_dropdown("Controllo Patogeni", "dd-patogeni", OPTIONS_PATOGENI, 'integrata', width="4"),
                create_dropdown("Sistema di Coltura", "dd-sistema-colturale", OPTIONS_SISTEMA, 'suolo_tradizionale',
                                width="4")
            ], className="mb-3"),
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
    ], align="end", className="mb-4"),

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
                    html.H4("Spiegazione del Grafico", id="titolo-spiegazione"),
                    html.Hr(),
                    dcc.Markdown(id="testo-spiegazione",
                                 children="*Seleziona una vista o modifica i parametri per visualizzare l'analisi...*")
                ], width=4, className="explanation-column"),

                dbc.Col([
                    html.Div(
                        id='container-produttivo',
                        style={'display': 'block', 'width': '100%'},
                        children=[
                            dcc.Graph(id='grafico-produttivo', style={'height': '50vh'}, animate=True)
                        ]
                    ),
                    html.Div(
                        id='container-risorse',
                        style={'display': 'none', 'width': '100%'},
                        children=[
                            dcc.Graph(id='grafico-risorse', style={'height': '50vh'}, animate=True)
                        ]
                    ),
                    html.Div(
                        id='container-finanziario',
                        style={'display': 'none', 'width': '100%'},
                        children=[
                            dbc.Card(
                                dbc.CardBody([
                                    html.H5("Fattori Variabili", className="card-title text-center"),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label("Costo Acqua (€/m³)", className="form-label"),
                                            dcc.Input(id='input-costo-acqua', type='number', value=1.00, step=0.01, className="form-control")
                                        ], width=3),
                                        dbc.Col([
                                            html.Label("Costo Fertilizzanti (€/kg)", className="form-label"),
                                            dcc.Input(id='input-costo-fertilizzanti', type='number', value=2.50, step=0.01, className="form-control")
                                        ], width=3),
                                        dbc.Col([
                                            html.Label("Altri Costi Variabili (€/Ha)", className="form-label"),
                                            dcc.Input(id='input-costi-extra', type='number', value=5000, step=100, className="form-control")
                                        ], width=3),
                                        dbc.Col([
                                            html.Label("Prezzo di Vendita (€/kg)", className="form-label"),
                                            dcc.Input(id='input-prezzo-vendita', type='number', value=3.50, step=0.05, className="form-control")
                                        ], width=3)
                                    ]),
                                ]),
                                className="mb-4",
                            ),
                            dbc.Row([
                                dbc.Col(dcc.Graph(id='grafico-sankey-finanziario',
                                                  # animate=True
                                                  ), width=6),
                                dbc.Col(dcc.Graph(id='grafico-composizione-costi',
                                                  # animate=True
                                                  ), width=6)
                            ], style={'height': '50vh'})
                        ]
                    ),
                ], width=8, className="p-3")
            ])
        ]),
        className="main-content-card"
    ),

    # Modale per la tabella mensile
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Distribuzione Mensile della Produzione")),
        dbc.ModalBody(id="contenuto-tabella-mensile"),
        dbc.ModalFooter(dbc.Button("Chiudi", id="btn-chiudi-modale", className="ms-auto", n_clicks=0)),
    ], id="modale-tabella-mensile", size="xl", is_open=False),

    # Modale per l'info impollinazione
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Info: Impollinazione Controllata con Bombi")),
        dbc.ModalBody(id="contenuto-info-impollinazione"),
        dbc.ModalFooter(dbc.Button("Chiudi", id="btn-chiudi-modal-impollinazione", n_clicks=0)),
    ],
        id="modal-info-impollinazione",
        size="xl",
        is_open=False,
    )
], fluid=True)
