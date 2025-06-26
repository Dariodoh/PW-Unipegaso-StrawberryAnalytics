from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app  # Importa l'istanza 'app' per usare le risorse (es. logo)


# --- Funzione Helper per creare i dropdown in modo pulito ---
# Questo aiuta a non ripetere lo stesso codice per ogni dropdown.
def create_dropdown(title, control_id):
    """Crea un label e un dropdown per il pannello di controllo."""
    return dbc.Col(
        html.Div([
            html.Label(f"{title}:"),
            dcc.Dropdown(
                id=control_id,
                options=[
                    {'label': 'Valore Basso', 'value': 'low'},
                    {'label': 'Valore Medio', 'value': 'medium'},
                    {'label': 'Valore Alto', 'value': 'high'},
                ],
                value='medium',  # Valore di default
                clearable=False,
                className="dropdown-dark"  # Classe custom per lo stile se necessario
            )
        ]),
        width=4  # 3 dropdown per riga (4*3 = 12 colonne)
    )


# --- Definizione del Layout Principale ---
# L'intera app è contenuta in un dbc.Container fluido per occupare tutta la larghezza.
layout = dbc.Container([

    # 1. Header con Logo Centrato
    dbc.Row([
        dbc.Col(
            html.Img(src=app.get_asset_url('logo.png'), height="200px"),
            width=48,
            className="mb-4 mt-4 d-flex justify-content-center"
        )
    ]),

    # 2. Pannello di Controllo con i 9 Dropdown
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                create_dropdown("Temperatura", "dd-temperatura"),
                create_dropdown("Luce", "dd-luce"),
                create_dropdown("Irrigazione", "dd-irrigazione"),
            ], className="mb-3"),
            dbc.Row([
                create_dropdown("Fertilizzazione", "dd-fertilizzazione"),
                create_dropdown("Controllo Patogeni", "dd-patogeni"),
                create_dropdown("Frequenza Raccolta", "dd-frequenza-raccolta"),
            ], className="mb-3"),
            dbc.Row([
                create_dropdown("Impollinazione Controllata", "dd-impollinazione"),
                create_dropdown("Densità di Coltivazione", "dd-densita"),
                create_dropdown("Numero di Impianti", "dd-impianti"),
            ])
        ]),
        className="mb-4"
    ),

    # 3. Pulsanti di Preset e Azioni Rapide
    dbc.Row([
        # Colonna per il primo gruppo di preset
        dbc.Col([
            html.H4("Preset per tipo di coltura"),
            dbc.ButtonGroup([
                dbc.Button("Tradizionale", id="btn-preset-tradizionale", n_clicks=0, outline=True, color="secondary"),
                dbc.Button("Soilless", id="btn-preset-soilless", n_clicks=0, outline=True, color="secondary"),
                dbc.Button("Idroponica", id="btn-preset-idroponica", n_clicks=0, outline=True, color="secondary"),
            ])
        ], width=5),  # Occupiamo 5/12 della larghezza

        # Colonna per il secondo gruppo di preset
        dbc.Col([
            html.H4("Preset per condizioni"),
            dbc.ButtonGroup([
                dbc.Button("Sfavorevoli", id="btn-preset-sfavorevoli", n_clicks=0, outline=True, color="secondary"),
                dbc.Button("Medie", id="btn-preset-medie", n_clicks=0, outline=True, color="secondary"),
                dbc.Button("Ottimali", id="btn-preset-ottimali", n_clicks=0, outline=True, color="secondary"),
            ])
        ], width=5),  # Occupiamo altri 5/12 della larghezza

        # Colonna destra per il pulsante singolo "alto"
        dbc.Col([
            dbc.Button(
                "Distribuzione Mensile",
                id="btn-distribuzione-mensile",
                n_clicks=0,
                outline=True,
                color="info",
                className="tall-button"  # Usiamo ancora la classe CSS per l'altezza
            )
        ],
            width=2,  # Occupiamo i restanti 2/12
            # Applichiamo flexbox per centrare il pulsante verticalmente
            className="d-flex align-items-center"
        )
    ],
        # Applichiamo flexbox alla riga intera per allineare verticalmente tutte le colonne
        # 'align-items-stretch' è l'impostazione predefinita, ma esplicitarla aiuta
        # 'align-items-end' potrebbe essere un'alternativa se vogliamo allineare tutto in basso
        align="center",
        className="mb-4"
    ),

    html.Hr(),  # Linea di separazione

    # 4. Selettore Vista Grafico (Tabs) e Area Contenuti
    dcc.Tabs(id="tabs-viste-grafici", value='tab-produttivo', children=[
        dcc.Tab(label='Andamento Produttivo', value='tab-produttivo'),
        dcc.Tab(label='Uso delle Risorse', value='tab-risorse'),
        dcc.Tab(label='Performance Finanziaria', value='tab-finanziaria'),
    ], className="mb-3"),

    # Riga che contiene spiegazione e grafico
    dbc.Row([
        # Colonna sinistra per la spiegazione del grafico
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Spiegazione del Grafico", id="titolo-spiegazione"),
                    html.Hr(),
                    dcc.Markdown(id="testo-spiegazione",
                                 children="*Seleziona una vista o modifica i parametri per visualizzare l'analisi...*")
                ])
            )
        ], width=3),

        # Colonna destra per il grafico principale
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    # Il grafico vero e proprio sarà inserito qui dalla callback
                    dcc.Graph(id='grafico-principale', style={'height': '50vh'})
                ])
            )
        ], width=9)
    ]),

    # 5. Modale (Pop-up) per la tabella mensile. Invisibile di default.
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Distribuzione Mensile della Produzione")),
            dbc.ModalBody(
                # Il contenuto (la tabella) sarà inserito qui dalla callback
                id="contenuto-tabella-mensile"
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Chiudi", id="btn-chiudi-modale", className="ms-auto", n_clicks=0
                )
            ),
        ],
        id="modale-tabella-mensile",
        size="lg",  # Dimensioni del pop-up: "sm", "lg", "xl"
        is_open=False,  # Il modale è chiuso di default
    ),

], fluid=True)