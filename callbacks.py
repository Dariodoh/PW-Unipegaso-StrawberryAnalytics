from dash import Input, Output, State, callback_context
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html # Importa html per creare la tabella

from app import app # Importa l'istanza dell'app
from data import df, get_dati_mensili # Importa il DataFrame e la funzione

@app.callback(
    [
        Output('kpi-row', 'children'),
        Output('grafico-andamento-temporale', 'figure'),
        Output('grafico-qualita', 'figure'),
        Output('grafico-canale', 'figure')
    ],
    [
        Input('filtro-appezzamento', 'value'),
        Input('filtro-canale', 'value'),
        Input('filtro-data', 'start_date'),
        Input('filtro-data', 'end_date')
    ]
)
def update_dashboard(appezzamenti_selezionati, canali_selezionati, data_inizio, data_fine):
    df_filtrato = df[
        (df['Appezzamento'].isin(appezzamenti_selezionati)) &
        (df['Canale Vendita'].isin(canali_selezionati)) &
        (df['Data'] >= data_inizio) &
        (df['Data'] <= data_fine)
        ]

    if df_filtrato.empty:
        empty_kpi = dbc.Alert("Nessun dato disponibile per i filtri selezionati.", color="warning")
        empty_fig = {'data': [], 'layout': {}}
        return [empty_kpi], empty_fig, empty_fig, empty_fig

    # Calcolo KPI
    totale_raccolto = int(df_filtrato['Quantità Raccolta (kg)'].sum())
    ricavo_totale = int(df_filtrato['Ricavo (€)'].sum())
    profitto_totale = int(df_filtrato['Profitto (€)'].sum())
    prezzo_medio = df_filtrato[df_filtrato['Ricavo (€)'] > 0]['Prezzo Vendita (€/kg)'].mean()

    kpi_cards = [
        dbc.Col(dbc.Card(
            [dbc.CardBody([html.H4("🍓 Raccolto Totale"), html.H5(f"{totale_raccolto} kg", className="text-success")])]),
                width=3),
        dbc.Col(dbc.Card(
            [dbc.CardBody([html.H4("💰 Ricavo Totale"), html.H5(f"€ {ricavo_totale:,}", className="text-success")])]),
                width=3),
        dbc.Col(dbc.Card([dbc.CardBody(
            [html.H4("📈 Profitto Totale"), html.H5(f"€ {profitto_totale:,}", className="text-success")])]), width=3),
        dbc.Col(dbc.Card(
            [dbc.CardBody([html.H4("💶 Prezzo Medio"), html.H5(f"€ {prezzo_medio:.2f}/kg", className="text-success")])]),
                width=3),
    ]

    # Creazione Grafici
    df_giornaliero = df_filtrato.groupby(df_filtrato['Data'].dt.date).agg(
        {'Quantità Raccolta (kg)': 'sum', 'Ricavo (€)': 'sum'}).reset_index()
    fig_andamento_temporale = px.line(
        df_giornaliero, x='Data', y=['Quantità Raccolta (kg)', 'Ricavo (€)'],
        title='Andamento Giornaliero Raccolto e Ricavo'
    )

    df_qualita = df_filtrato.groupby('Qualità')['Quantità Raccolta (kg)'].sum().reset_index()
    fig_qualita = px.pie(
        df_qualita, names='Qualità', values='Quantità Raccolta (kg)',
        title='Distribuzione del Raccolto per Qualità',
        color_discrete_map={'Prima Scelta': 'green', 'Seconda Scelta': 'orange', 'Scarto': 'red'}
    )

    df_canale = df_filtrato.groupby('Canale Vendita')['Ricavo (€)'].sum().reset_index()
    fig_canale = px.bar(
        df_canale, x='Canale Vendita', y='Ricavo (€)',
        title='Ricavi per Canale di Vendita', text_auto='.2s'
    )

    return kpi_cards, fig_andamento_temporale, fig_qualita, fig_canale


@app.callback(
    Output("modale-tabella-mensile", "is_open"),
    Output("contenuto-tabella-mensile", "children"),
    [
        Input("btn-distribuzione-mensile", "n_clicks"),
        Input("btn-chiudi-modale", "n_clicks"),
    ],
    [
        State("modale-tabella-mensile", "is_open"),
        # Usiamo State per prendere i valori dei filtri senza che la callback si attivi al loro cambio
        State('filtro-appezzamento', 'value'),
        State('filtro-canale', 'value'),
        State('filtro-data', 'start_date'),
        State('filtro-data', 'end_date')
    ],
    prevent_initial_call=True  # Non eseguire questa callback al caricamento iniziale
)
def toggle_and_fill_modal(n_open, n_close, is_open, appezzamenti, canali, start_date, end_date):
    # Chi ha attivato la callback?
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    # Se il pulsante "Distribuzione Mensile" è stato premuto
    if triggered_id == "btn-distribuzione-mensile":
        # Filtra i dati in base alla selezione corrente nei filtri
        df_filtrato = df[
            (df['Appezzamento'].isin(appezzamenti)) &
            (df['Canale Vendita'].isin(canali)) &
            (df['Data'] >= start_date) &
            (df['Data'] <= end_date)
            ]

        # Usa la funzione di data.py per ottenere il riepilogo mensile
        df_mensile = get_dati_mensili(df_filtrato)

        if df_mensile.empty:
            tabella = html.P("Nessun dato da mostrare per i filtri selezionati.")
        else:
            # Crea una tabella Bootstrap-styled
            tabella = dbc.Table.from_dataframe(
                df_mensile,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True
            )

        return True, tabella  # Apri il modale (is_open=True) e inserisci la tabella

    # Se il pulsante "Chiudi" o qualsiasi altra cosa ha attivato la callback
    if triggered_id == "btn-chiudi-modale" or is_open:
        return False, []  # Chiudi il modale (is_open=False) e svuota il contenuto

    return is_open, []