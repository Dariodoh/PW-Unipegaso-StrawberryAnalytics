# file: layout.py

from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app  # Importa l'istanza 'app' per usare le risorse (es. logo)


# --- Funzione Helper per creare i dropdown in modo pulito ---
def create_dropdown(title, control_id, info_button_id=None):
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
            html.Div(label_content, className="d-flex align-items-center mb-2"),  # Allinea label e bottone
            dcc.Dropdown(
                id=control_id,
                options=[
                    {'label': 'Valore Basso', 'value': 'low'},
                    {'label': 'Valore Medio', 'value': 'medium'},
                    {'label': 'Valore Alto', 'value': 'high'},
                ],
                value='medium',
                clearable=False
            )
        ]),
        width=4
    )


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
                create_dropdown("Temperatura", "dd-temperatura"),
                create_dropdown("Irraggiamento solare", "dd-luce"),
                create_dropdown("Irrigazione", "dd-irrigazione"),
            ], className="mb-3"),
            dbc.Row([
                create_dropdown("Fertilizzazione", "dd-fertilizzazione"),
                create_dropdown("Controllo Patogeni", "dd-patogeni"),
                create_dropdown("Frequenza Raccolta", "dd-frequenza-raccolta"),
            ], className="mb-3"),
            dbc.Row([
                create_dropdown(
                    "Impollinazione Controllata",
                    "dd-impollinazione",
                    info_button_id="btn-info-impollinazione"
                ),
                create_dropdown("Densità di Coltivazione", "dd-densita"),
                create_dropdown("Numero di Impianti", "dd-impianti"),
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
    ], className="mb-3"),
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4("Spiegazione del Grafico", id="titolo-spiegazione"),
                html.Hr(),
                dcc.Markdown(id="testo-spiegazione",
                             children="*Seleziona una vista o modifica i parametri per visualizzare l'analisi...*")
            ]))
        ], width=3),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-principale', style={'height': '50vh'})
            ]))
        ], width=9)
    ]),

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