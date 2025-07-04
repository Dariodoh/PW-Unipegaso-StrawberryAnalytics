# file: data.py

import pandas as pd
import numpy as np

PRODUZIONE_BASE_OTTIMALE = 10.0  # kg/m², potenziale massimo teorico stagionale
CONSUMO_OTTIMALE_ACQUA = 500.0 # l/m², consumo ottimale stagionale d'acqua
CONSUMO_OTTIMALE_FERT = 0.07 # kg/m², consumo otimale stagionale di fertilizzanti
BENCHMARK_OTTIMALI = {'acqua': 500.0, # l/m², consumo ottimale stagionale d'acqua
                      'fertilizzanti': 0.07 } # kg/m², consumo ottimale stagionale di fertilizzanti
PREZZO_VENDITA_FRAGOLE_AL_KG = 3.50      # Prezzo medio di vendita in €/kg
COSTO_ACQUA_AL_METRO_CUBO = 1.00         # Costo dell'acqua in €/m³ (1 m³ = 1000 litri)
COSTO_FERTILIZZANTI_AL_KG = 2.50         # Costo dei fertilizzanti in €/kg
COSTI_VARIABILI_EXTRA_PER_ETTARO = 5000  # Stima di altri costi (manodopera, etc.) in €/Ha

PESI_FATTORI = {
    'dd-temperatura': {'ottimale': (0.95, 1.0), 'sub-freddo': (0.7, 0.85), 'sub-caldo': (0.6, 0.75),'critico': (0.2, 0.4)},
    'dd-luce': {'alta': (0.95, 1.0), 'media': (0.8, 0.9), 'bassa': (0.5, 0.7)},
    'dd-irrigazione': {'goccia': (0.98, 1.0), 'aspersione': (0.75, 0.85), 'manuale': (0.6, 0.7)},
    'dd-fertilizzazione': {'idroponica': (1.0, 1.0), 'fertirrigazione': (0.85, 0.95), 'organica': (0.65, 0.8)},
    'dd-patogeni': {'integrata': (0.9, 1.0), 'biologico': (0.75, 0.85), 'convenzionale': (0.8, 0.9)},
    'dd-frequenza-raccolta': {'alta': (0.95, 1.0), 'media': (0.8, 0.9), 'bassa': (0.6, 0.75)},
    'dd-impollinazione': {'bombi': (0.98, 1.0), 'naturale': (0.7, 0.85), 'manuale': (0.4, 0.6)},
    'dd-umidita': {'ottimale': (0.95, 1.0), 'alta_rischiosa': (0.6, 0.8), 'bassa_stress': (0.7, 0.85)},
    'dd-sistema-colturale': {'suolo_tradizionale': (0.9, 1.0),'soilless_aperto': (1.1, 1.2),'idroponico_ricircolo': (1.2, 1.35)}
}

IMPATTI_RISORSE = {
    'dd-temperatura': {
        'ottimale': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'sub-freddo': {'acqua': 0.9, 'fertilizzanti': 0.95},
        'sub-caldo': {'acqua': 1.25, 'fertilizzanti': 1.0},
        'critico': {'acqua': 1.4, 'fertilizzanti': 0.8},
    },
    'dd-luce': {
        'alta': {'acqua': 1.0, 'fertilizzanti': 1.1},
        'media': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'bassa': {'acqua': 0.95, 'fertilizzanti': 0.9},
    },
    'dd-umidita': {
        'ottimale': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'alta_rischiosa': {'acqua': 0.85, 'fertilizzanti': 1.0},
        'bassa_stress': {'acqua': 1.3, 'fertilizzanti': 1.0},
    },
    'dd-irrigazione': {
        'goccia': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'aspersione': {'acqua': 1.4, 'fertilizzanti': 1.2},
        'manuale': {'acqua': 2.0, 'fertilizzanti': 1.5},
    },
    'dd-fertilizzazione': {
        'idroponica': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'fertirrigazione': {'acqua': 1.05, 'fertilizzanti': 1.15},
        'organica': {'acqua': 1.1, 'fertilizzanti': 1.3},
    },
    'dd-patogeni': {
        'integrata': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'biologica': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'convenzionale': {'acqua': 1.0, 'fertilizzanti': 1.0},
    },
    'dd-frequenza-raccolta': {
        'alta': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'media': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'bassa': {'acqua': 1.0, 'fertilizzanti': 1.0},
    },
    'dd-impollinazione': {
        'bombi': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'manuale': {'acqua': 1.0, 'fertilizzanti': 1.0},
        'naturale': {'acqua': 1.0, 'fertilizzanti': 1.0},
    },
    'dd-sistema-colturale': {
        'suolo_tradizionale': {'acqua': 1.5, 'fertilizzanti': 1.4}, # Meno efficiente
        'soilless_aperto': {'acqua': 0.8, 'fertilizzanti': 0.7}, # Molto efficiente
        'idroponico_ricircolo': {'acqua': 0.15, 'fertilizzanti': 0.4}, # Estremamente efficiente
    },
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


def simula_consumo_risorse(fattori: dict) -> tuple[dict, dict]:
    """
    Simula il consumo di acqua e fertilizzanti basandosi sul modello IMPATTI_RISORSE.
    """

    fattore_acqua = 1.0
    fattore_fertilizzanti = 1.0

    # Calcola l'impatto usando il dizionario dedicato IMPATTI_RISORSE
    for id_fattore, valore_selezionato in fattori.items():
        if id_fattore in IMPATTI_RISORSE and valore_selezionato in IMPATTI_RISORSE[id_fattore]:
            pesi = IMPATTI_RISORSE[id_fattore][valore_selezionato]
            fattore_acqua *= pesi['acqua']
            fattore_fertilizzanti *= pesi['fertilizzanti']

    consumi_stimati = {
        'acqua': BENCHMARK_OTTIMALI['acqua'] * fattore_acqua,
        'fertilizzanti': BENCHMARK_OTTIMALI['fertilizzanti'] * fattore_fertilizzanti
    }

    return consumi_stimati, BENCHMARK_OTTIMALI


def simula_performance_finanziaria(produzione_kg_mq, consumi_risorse_mq):
    """
    Simula la performance finanziaria per metro quadro (m²).

    Args:
        produzione_kg_mq (float): La produzione stimata in kg/m².
        consumi_risorse_mq (dict): Un dizionario con i consumi per m² di
                                   'acqua' (litri) e 'fertilizzanti' (kg).

    Returns:
        dict: Un dizionario con Ricavi, Costi e Profitto Lordo, tutto per m².
    """
    # 1. Calcolo Ricavi per m²
    ricavi_mq = produzione_kg_mq * PREZZO_VENDITA_FRAGOLE_AL_KG

    # 2. Calcolo Costi per m²
    # Converti consumo acqua da litri a metri cubi (1000L = 1m³)
    costo_acqua_mq = (consumi_risorse_mq['acqua'] / 1000) * COSTO_ACQUA_AL_METRO_CUBO
    costo_fertilizzanti_mq = consumi_risorse_mq['fertilizzanti'] * COSTO_FERTILIZZANTI_AL_KG

    # Converti costi extra da €/Ha a €/m² (1 Ha = 10.000 m²)
    altri_costi_mq = COSTI_VARIABILI_EXTRA_PER_ETTARO / 10000

    costi_totali_mq = costo_acqua_mq + costo_fertilizzanti_mq + altri_costi_mq

    # 3. Calcolo Profitto Lordo per m²
    profitto_lordo_mq = ricavi_mq - costi_totali_mq

    # Restituisce un dizionario pronto per il grafico a cascata
    return {
        "Ricavi (€/m²)": ricavi_mq,
        "Costo Acqua": costo_acqua_mq,
        "Costo Fertilizzanti": costo_fertilizzanti_mq,
        "Altri Costi": altri_costi_mq,
        "Profitto Lordo (€/m²)": profitto_lordo_mq
    }

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
