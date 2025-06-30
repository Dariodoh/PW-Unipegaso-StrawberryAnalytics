# file: data.py

import pandas as pd
import numpy as np


def genera_dati_fittizi():
    """Genera un DataFrame fittizio per l'analisi delle fragole."""
    date_range = pd.to_datetime(pd.date_range(start="2023-01-01", end="2023-07-31"))
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


def get_calendario_colturale_fragola():
    """
    Restituisce un DataFrame statico con il calendario colturale della fragola
    nel Metapontino, basato su dati reali e articoli di settore.
    """
    dati_calendario = [
        {"Mese": "Gennaio", "Peso (%)": "5%",
         "Descrizione": "Ripresa vegetativa e avvio raccolte delle varietà più precoci"},
        {"Mese": "Febbraio", "Peso (%)": "8%",
         "Descrizione": "Intensificazione delle prime raccolte, piena fioritura"},
        {"Mese": "Marzo", "Peso (%)": "18%",
         "Descrizione": "Inizio del picco produttivo per le principali cultivar come la Candonga"},
        {"Mese": "Aprile", "Peso (%)": "28%",
         "Descrizione": "Picco massimo della campagna di raccolta, massima richiesta di mercato"},
        {"Mese": "Maggio", "Peso (%)": "23%",
         "Descrizione": "Piena produzione, inizio della fase calante verso la fine del mese"},
        {"Mese": "Giugno", "Peso (%)": "8%",
         "Descrizione": "Raccolte tardive e conclusione della campagna di produzione"},
        {"Mese": "Luglio", "Peso (%)": "2%",
         "Descrizione": "Fine completa delle raccolte, estirpo delle piante e preparazione terreni"},
        {"Mese": "Agosto", "Peso (%)": "2%",
         "Descrizione": "Pratiche agronomiche: solarizzazione del terreno per la disinfezione"},
        {"Mese": "Settembre", "Peso (%)": "2%",
         "Descrizione": "Preparazione del suolo e inizio trapianti per il nuovo ciclo produttivo"},
        {"Mese": "Ottobre", "Peso (%)": "2%",
         "Descrizione": "Fase principale dei trapianti delle nuove piantine radicate"},
        {"Mese": "Novembre", "Peso (%)": "1%", "Descrizione": "Sviluppo vegetativo iniziale delle nuove piante"},
        {"Mese": "Dicembre", "Peso (%)": "1%",
         "Descrizione": "Fase di riposo vegetativo o crescita minima in attesa della ripresa"},
    ]

    df_calendario = pd.DataFrame(dati_calendario)

    df_calendario.rename(columns={
        'Mese': 'Mese',
        'Peso': 'Peso (%)',
        'Descrizione': 'Descrizione Attività'
    }, inplace=True)

    return df_calendario