# file: data.py

import pandas as pd
import numpy as np


def genera_dati_fittizi():
    """Genera un DataFrame fittizio per l'analisi delle fragole."""
    date_range = pd.to_datetime(pd.date_range(start="2023-04-01", end="2023-06-30"))
    n_records = len(date_range) * 3

    data = {
        'Data': np.random.choice(date_range, n_records),
        'Appezzamento': np.random.choice(['Campo Nord', 'Serra A', 'Campo Est', 'Serra B'], n_records),
        'Quantità Raccolta (kg)': np.random.uniform(20, 100, n_records),
        'Qualità': np.random.choice(['Prima Scelta', 'Seconda Scelta', 'Scarto'], n_records, p=[0.7, 0.2, 0.1]),
        'Prezzo Vendita (€/kg)': np.random.uniform(3.5, 6.0, n_records),
        'Canale Vendita': np.random.choice(['GDO', 'Mercati Locali', 'Export'], n_records, p=[0.5, 0.3, 0.2]),
    }
    df = pd.DataFrame(data)

    df['Ricavo (€)'] = df['Quantità Raccolta (kg)'] * df['Prezzo Vendita (€/kg)']
    df['Costo Produzione (€/kg)'] = df['Prezzo Vendita (€/kg)'] * np.random.uniform(0.4, 0.6)
    df['Costo Totale (€)'] = df['Quantità Raccolta (kg)'] * df['Costo Produzione (€/kg)']
    df['Profitto (€)'] = df['Ricavo (€)'] - df['Costo Totale (€)']

    df.loc[df['Qualità'] == 'Scarto', 'Ricavo (€)'] = 0
    df.loc[df['Qualità'] == 'Scarto', 'Profitto (€)'] = -df['Costo Totale (€)']
    df.loc[df['Qualità'] == 'Scarto', 'Canale Vendita'] = 'Non Venduto'

    return df.sort_values(by="Data").reset_index(drop=True)


# Creiamo il DataFrame una sola volta e lo rendiamo disponibile per l'importazione
df = genera_dati_fittizi()


def get_dati_mensili(dataframe):
    """
    Aggrega il DataFrame su base mensile, calcolando totali e medie.
    Restituisce un nuovo DataFrame pronto per essere visualizzato in una tabella.
    """
    if dataframe.empty:
        return pd.DataFrame()  # Restituisce un df vuoto se non ci sono dati

    df_mensile = dataframe.copy()
    df_mensile['Mese'] = df_mensile['Data'].dt.to_period('M')

    # Aggregazione
    summary = df_mensile.groupby('Mese').agg(
        Raccolto_Totale_kg=('Quantità Raccolta (kg)', 'sum'),
        Ricavo_Totale_Euro=('Ricavo (€)', 'sum'),
        Profitto_Totale_Euro=('Profitto (€)', 'sum'),
        Prezzo_Medio_Euro_kg=('Prezzo Vendita (€/kg)', 'mean')
    ).reset_index()

    # Formattazione per la visualizzazione
    summary['Mese'] = summary['Mese'].dt.strftime('%B %Y')  # Formato "Mese Anno"
    summary['Raccolto_Totale_kg'] = summary['Raccolto_Totale_kg'].round(0).astype(int)
    summary['Ricavo_Totale_Euro'] = summary['Ricavo_Totale_Euro'].round(0).astype(int)
    summary['Profitto_Totale_Euro'] = summary['Profitto_Totale_Euro'].round(0).astype(int)
    summary['Prezzo_Medio_Euro_kg'] = summary['Prezzo_Medio_Euro_kg'].round(2)

    # Rinomina colonne per chiarezza
    summary.rename(columns={
        'Raccolto_Totale_kg': 'Raccolto (kg)',
        'Ricavo_Totale_Euro': 'Ricavo (€)',
        'Profitto_Totale_Euro': 'Profitto (€)',
        'Prezzo_Medio_Euro_kg': 'Prezzo Medio (€/kg)'
    }, inplace=True)

    return summary