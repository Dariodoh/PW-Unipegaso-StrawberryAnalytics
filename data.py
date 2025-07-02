# file: data.py

import pandas as pd
import numpy as np

PRODUZIONE_BASE_OTTIMALE = 10.0  # kg/m², potenziale massimo teorico

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


def prepare_benchmark_dataframe(fattori: dict) -> tuple[pd.DataFrame, float]:
    """
    Calcola la produzione simulata e la confronta con i benchmark,
    restituendo un DataFrame pronto per il plotting e il valore simulato.

    Args:
        fattori (dict): Il dizionario con i valori selezionati dai dropdown.

    Returns:
        tuple[pd.DataFrame, float]: Un DataFrame per il grafico a barre e
                                      il valore numerico della produzione simulata.
    """
    # 1. Calcola il valore della produzione simulata
    produzione_simulata = simula_produzione_annua(fattori)

    # 2. Definisce i benchmark di confronto
    benchmark = {'Sfavorevole': 3.0, 'Media': 5.5, 'Ottimale': 8.5}

    # 3. Prepara i dati per il DataFrame
    data_to_plot = {
        'Scenario': ['Produzione Stimata', 'Produzione Media', 'Produzione Ottimale', 'Produzione Sfavorevole'],
        'Produzione (kg/m²)': [
            produzione_simulata,
            benchmark['Media'],
            benchmark['Ottimale'],
            benchmark['Sfavorevole']
        ]
    }

    # 4. Crea il DataFrame
    df_plot = pd.DataFrame(data_to_plot)

    # 5. Restituisce sia il DataFrame che il valore numerico
    return df_plot, produzione_simulata

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