from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app


# --- Funzione Helper per creare i dropdown ---
def create_dropdown(title, control_id, options, default_value, col_args, info_button_id=None):
    """
    Crea un label (con un pulsante info opzionale) e un dropdown.
    """
    label_content = [html.Label(f"{title}:", className="form-label")]
    if info_button_id:
        # Creazione del bottone INFO se viene passato un button_id
        label_content.append(
            html.Button(
                "info", id=info_button_id,
                # size="sm",
                # color="info",
                className="btn btn-info btn-sm rounded-circle ms-2 info-button-custom", n_clicks=0,
                **{"aria-label": f"Maggiori informazioni su {title}"}
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
        **col_args,
        className="mb-3"
    )


# --- Opzioni per i dropdown ---
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
    {'label': 'In Suolo/Tradizionale', 'value': 'suolo_tradizionale'},
    {'label': 'Fuori Suolo (Drenaggio a perdere)', 'value': 'soilless_aperto'},
    {'label': 'Idroponico (Ricircolo)', 'value': 'idroponico_ricircolo'},
]

# --- Layout Principale ---
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('logo.jpg'), height="150px",
                         alt="Logo di Strawberry Analytics: una fragola stilizzata con grafici"),
                width=12,
                className="mb-4 mt-4 d-flex justify-content-center")
    ]),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                create_dropdown("Temperatura", "dd-temperatura", OPTIONS_TEMPERATURA, 'ottimale',
                                col_args={'lg': 2, 'md': 4, 'sm': 6}),
                create_dropdown("Luce", "dd-luce", OPTIONS_LUCE, 'media', col_args={'lg': 2, 'md': 4, 'sm': 6}),
                create_dropdown("Umidità Relativa", "dd-umidita", OPTIONS_UMIDITA, 'ottimale',
                                col_args={'lg': 2, 'md': 4, 'sm': 6}),
                create_dropdown("Fertilizzazione", "dd-fertilizzazione", OPTIONS_FERTILIZZAZIONE, 'fertirrigazione',
                                col_args={'lg': 2, 'md': 4, 'sm': 6}),
                create_dropdown("Frequenza Raccolta", "dd-frequenza-raccolta", OPTIONS_RACCOLTA, 'media',
                                col_args={'lg': 2, 'md': 4, 'sm': 6}),
                create_dropdown("Impollinazione", "dd-impollinazione", OPTIONS_IMPOLLINAZIONE, 'bombi',
                                info_button_id="btn-info-impollinazione", col_args={'lg': 2, 'md': 4, 'sm': 6}),
            ]),
            dbc.Row([
                create_dropdown("Irrigazione", "dd-irrigazione", OPTIONS_IRRIGAZIONE, 'goccia',
                                col_args={'lg': 2, 'md': 4, 'sm': 6}),
                create_dropdown("Controllo Patogeni", "dd-patogeni", OPTIONS_PATOGENI, 'integrata',
                                info_button_id="btn-info-patogeni", col_args={'lg': 2, 'md': 4, 'sm': 6}),
                create_dropdown("Sistema di Coltura", "dd-sistema-colturale", OPTIONS_SISTEMA, 'suolo_tradizionale',
                                info_button_id="btn-info-coltura", col_args={'lg': 2, 'md': 4, 'sm': 6})
            ]),
        ]),
        className="mb-4 dropdown-panel-card"
    ),

    dbc.Row([
        # Preset tipo di coltura
        dbc.Col([
            html.H4("Preset per tipo di coltura"),
            dbc.ButtonGroup([
                dbc.Button("Tradizionale", id="btn-preset-tradizionale", n_clicks=0, className="custom-button-green"),
                dbc.Button("Soilless", id="btn-preset-soilless", n_clicks=0, className="custom-button-green"),
                dbc.Button("Idroponica", id="btn-preset-idroponica", n_clicks=0, className="custom-button-green"),
            ])
        ], lg=5, md=12, className="mb-3 mb-lg-0"),

        # Preset per condizioni sfavorevoli/medie/ottimali
        dbc.Col([
            html.H4("Preset per condizioni"),
            dbc.ButtonGroup([
                dbc.Button("Sfavorevoli", id="btn-preset-sfavorevoli", n_clicks=0, className="custom-button-green"),
                dbc.Button("Medie", id="btn-preset-medie", n_clicks=0, className="custom-button-green"),
                dbc.Button("Ottimali", id="btn-preset-ottimali", n_clicks=0, className="custom-button-green"),
            ])
        ], lg=5, md=12, className="mb-3 mb-lg-0"),

        # Pulsante Distribuzione Mensile
        dbc.Col([
            html.Div(
                dbc.Button("Distribuzione Mensile", id="btn-distribuzione-mensile", n_clicks=0,
                           className="custom-button-green w-100"),
                className="d-grid"
            )
        ], lg=2, md=12)
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
                # Colonna sinistra per il commento al grafico
                dbc.Col([
                    html.H4(id="titolo-commentary"),
                    html.Hr(),
                    dcc.Markdown(id="testo-commentary",
                                 children="*Seleziona una vista o modifica i parametri per visualizzare l'analisi...*")
                ], lg=4, md=12, style={'maxHeight': '700px', 'overflowY': 'auto', 'paddingRight': '15px'},
                    className="explanation-column mb-4 mb-lg-0"),

                # Colonna destra per il plot dei diversi grafici
                dbc.Col([
                    html.Div(
                        id='container-produttivo',
                        style={'display': 'block', 'width': '100%'},
                        children=[
                            dcc.Graph(id='grafico-produttivo', style={'height': '50vh'}, animate=True)
                        ],
                        role="figure",
                        **{
                            "aria-label": "Grafico dell'andamento produttivo delle fragole nel tempo.",
                            "aria-describedby": "testo-commentary"
                        }
                    ),
                    html.Div(
                        id='container-risorse',
                        style={'display': 'none', 'width': '100%'},
                        children=[
                            dcc.Graph(id='grafico-risorse', style={'height': '50vh'}, animate=True)
                        ],
                        role="figure",
                        **{
                            "aria-label": "Grafico sull'utilizzo delle risorse (acqua, fertilizzanti).",
                            "aria-describedby": "testo-commentary"
                        }
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
                                            dcc.Input(id='input-costo-acqua', type='number', value=1.00, step=0.01,
                                                      className="form-control")
                                        ], lg=3, md=6, sm=12, className="mb-3"),
                                        dbc.Col([
                                            html.Label("Costo Fertilizzanti (€/kg)", className="form-label"),
                                            dcc.Input(id='input-costo-fertilizzanti', type='number', value=2.50,
                                                      step=0.01, className="form-control")
                                        ], lg=3, md=6, sm=12, className="mb-3"),
                                        dbc.Col([
                                            html.Label("Altri Costi Variabili (€/Ha)", className="form-label"),
                                            dcc.Input(id='input-costi-extra', type='number', value=5000, step=100,
                                                      className="form-control")
                                        ], lg=3, md=6, sm=12, className="mb-3"),
                                        dbc.Col([
                                            html.Label("Prezzo di Vendita (€/kg)", className="form-label"),
                                            dcc.Input(id='input-prezzo-vendita', type='number', value=3.50, step=0.05,
                                                      className="form-control")
                                        ], lg=3, md=6, sm=12, className="mb-3")
                                    ]),
                                ]),
                                className="mb-4",
                            ),
                            dbc.Row([
                                dbc.Col(
                                    html.Div([
                                        dcc.Graph(id='grafico-sankey-finanziario',
                                                  )],
                                        role="figure",
                                        **{"aria-label": "Diagramma di Sankey che mostra i flussi di costi e ricavi."}
                                    ), lg=6, md=12, ),
                                dbc.Col(
                                    html.Div([
                                        dcc.Graph(id='grafico-composizione-costi',
                                                  )],
                                        role="figure",
                                        **{"aria-label": "Grafico a torta che mostra la composizione dei costi."}
                                    ), lg=6, md=12,
                                )
                            ])
                        ],
                        **{"aria-label": "Vista della performance finanziaria"}
                    ),
                ], lg=8, md=12, className="p-3")
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
        dbc.ModalHeader(dbc.ModalTitle("Impollinazione Controllata")),
        dbc.ModalBody(id="contenuto-info-impollinazione"),
        dbc.ModalFooter(dbc.Button("Chiudi", id="btn-chiudi-modal-impollinazione", n_clicks=0)),
    ],
        id="modal-info-impollinazione",
        size="xl",
        is_open=False,
    ),

    # Modale per l'info patogeni
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Controllo patogeni e Lotta Integrata")),
        dbc.ModalBody(id="contenuto-info-patogeni"),
        dbc.ModalFooter(dbc.Button("Chiudi", id="btn-chiudi-modal-patogeni", n_clicks=0)),
    ],
        id="modal-info-patogeni",
        size="xl",
        is_open=False,
    ),

    # Modale per l'info tipologia coltura
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Tipologia di Coltura")),
        dbc.ModalBody(id="contenuto-info-coltura"),
        dbc.ModalFooter(dbc.Button("Chiudi", id="btn-chiudi-modal-coltura", n_clicks=0)),
    ],
        id="modal-info-coltura",
        size="xl",
        is_open=False,
    )

], fluid=True)
