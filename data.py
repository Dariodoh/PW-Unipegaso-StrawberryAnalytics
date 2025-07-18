import pandas as pd
import numpy as np

PRODUZIONE_BASE_OTTIMALE = 10.0  # kg/m², potenziale massimo teorico stagionale
RANGE_OTTIMALE_ACQUA = (300, 450) # l/m², consumo ottimale stagionale d'acqua
RANGE_OTTIMALE_FERTILIZZANTI = (0.010, 0.015) # kg/m², consumo ottimale stagionale di fertilizzanti

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
        'ottimale': {'acqua': (-0.02, 0.02), 'fertilizzanti': (0.0, 0.0)},
        'sub-freddo': {'acqua': (-0.15, -0.05), 'fertilizzanti': (-0.1, -0.0)},
        'sub-caldo': {'acqua': (0.20, 0.30), 'fertilizzanti': (0.0, 0.0)},
        'critico': {'acqua': (0.35, 0.45), 'fertilizzanti': (-0.25, -0.15)}, # Stress idrico > consumo acqua; stress termico < assorbimento nutrienti
    },
    'dd-luce': {
        'alta': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.05, 0.15)},
        'media': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'bassa': {'acqua': (-0.1, -0.0), 'fertilizzanti': (-0.15, -0.05)},
    },
    'dd-umidita': {
        'ottimale': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'alta_rischiosa': {'acqua': (-0.2, -0.1), 'fertilizzanti': (0.0, 0.0)}, # Meno traspirazione
        'bassa_stress': {'acqua': (0.25, 0.35), 'fertilizzanti': (0.0, 0.0)}, # Più traspirazione
    },
    'dd-irrigazione': {
        'goccia': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'aspersione': {'acqua': (0.35, 0.45), 'fertilizzanti': (0.15, 0.25)},
        'manuale': {'acqua': (0.8, 1.2), 'fertilizzanti': (0.4, 0.6)},
    },
    'dd-fertilizzazione': {
        'idroponica': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)}, # L'impatto è già gestito da sistema-colturale
        'fertirrigazione': {'acqua': (0.0, 0.05), 'fertilizzanti': (0.1, 0.2)},
        'organica': {'acqua': (0.05, 0.15), 'fertilizzanti': (0.25, 0.35)},
    },
    'dd-patogeni': { # Impatto nullo sul consumo, ma sulla produzione
        'integrata': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'biologica': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'convenzionale': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
    },
    'dd-frequenza-raccolta': { # Impatto nullo sul consumo
        'alta': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'media': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'bassa': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
    },
    'dd-impollinazione': { # Impatto nullo sul consumo
        'bombi': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'manuale': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
        'naturale': {'acqua': (0.0, 0.0), 'fertilizzanti': (0.0, 0.0)},
    },
    'dd-sistema-colturale': {
        'suolo_tradizionale': {'acqua': (0.4, 0.6), 'fertilizzanti': (0.3, 0.5)},
        'soilless_aperto': {'acqua': (-0.25, -0.15), 'fertilizzanti': (-0.35, -0.25)},
        'idroponico_ricircolo': {'acqua': (-0.9, -0.8), 'fertilizzanti': (-0.65, -0.55)},
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
    Simula il consumo di risorse partendo da un range ottimale e applicando
    una somma di modificatori percentuali casuali basati sulle scelte agronomiche.
    Mantiene la struttura del dizionario IMPATTI_RISORSE.

    Args:
        fattori (dict): Un dizionario con le scelte per ogni fattore (es. {'dd-temperatura': 'sub-caldo'}).

    Returns:
        dict: Un dizionario con 'acqua' (l/mq) e 'fertilizzanti' (kg/mq).
    """

    mod_totale_acqua = 0.0
    mod_totale_fertilizzanti = 0.0

    consumo_base_acqua = np.random.uniform(*RANGE_OTTIMALE_ACQUA)
    consumo_base_fertilizzanti = np.random.uniform(*RANGE_OTTIMALE_FERTILIZZANTI)

    # Iterazione sui fattori scelti dall'utente per calcolarne la somma
    for id_fattore, scelta_utente in fattori.items():
        if id_fattore in IMPATTI_RISORSE and scelta_utente in IMPATTI_RISORSE[id_fattore]:
            modificatori = IMPATTI_RISORSE[id_fattore][scelta_utente]

            # Estrazione del range di modifica per l'acqua, scelta del valore casuale e somma
            range_mod_acqua = modificatori['acqua']
            mod_totale_acqua += np.random.uniform(*range_mod_acqua)

            # Estrazione del range di modifica per i fertilizzanti, scelta del valore casuale e somma
            range_mod_fertilizzanti = modificatori['fertilizzanti']
            mod_totale_fertilizzanti += np.random.uniform(*range_mod_fertilizzanti)

    #Modificatori totali applicati ai valori di base
    consumo_finale_acqua = consumo_base_acqua * (1 + mod_totale_acqua)
    consumo_finale_fertilizzanti = consumo_base_fertilizzanti * (1 + mod_totale_fertilizzanti)

    #Valori sempre postivi
    consumo_finale_acqua = max(0, consumo_finale_acqua)
    consumo_finale_fertilizzanti = max(0, consumo_finale_fertilizzanti)

    return {
        'acqua': consumo_finale_acqua,
        'fertilizzanti': consumo_finale_fertilizzanti
    }


def simula_performance_finanziaria(produzione_kg_mq, consumi_risorse_mq, prezzo_vendita_kg,
                                   costo_acqua_m3, costo_fert_kg, costi_extra_ha):
    """
    Simula la performance finanziaria per metro quadro (m²).

    Args:
        produzione_kg_mq (float): La produzione stimata in kg/m².
        consumi_risorse_mq (dict): Un dizionario con i consumi per m² di
                                   'acqua' (litri) e 'fertilizzanti' (kg).

    Returns:
        dict: Un dizionario con Ricavi, Costi e Profitto Lordo, tutto per m².
    """
    # Calcolo Ricavi per m²
    ricavi_mq = produzione_kg_mq * prezzo_vendita_kg

    # Calcolo Costi per m²
    # Conversione consumo acqua litri -> metri cubi
    costo_acqua_mq = (consumi_risorse_mq['acqua'] / 1000) * costo_acqua_m3
    costo_fertilizzanti_mq = consumi_risorse_mq['fertilizzanti'] * costo_fert_kg

    # Conversione costi extra €/Ha -> €/m²
    altri_costi_mq = costi_extra_ha / 10000

    costi_totali_mq = costo_acqua_mq + costo_fertilizzanti_mq + altri_costi_mq

    # Calcolo Profitto Lordo per m²
    profitto_lordo_mq = ricavi_mq - costi_totali_mq

    # Dizionario pronto per il grafico a cascata
    return {
        "Ricavi (€/m²)": ricavi_mq,
        "Costo Acqua": -costo_acqua_mq,
        "Costo Fertilizzanti": -costo_fertilizzanti_mq,
        "Altri Costi": -altri_costi_mq,
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
    # Calcolo del valore della produzione simulata
    produzione_simulata = simula_produzione_annua(fattori)

    # 2. Benchmark di confronto
    benchmark = {'Sfavorevole': 3.0, 'Media': 5.5, 'Ottimale': 8.5}

    # Preparazione dei dati per il DataFrame
    data_to_plot = {
        'Scenario': ['Produzione Stimata', 'Produzione Sfavorevole', 'Produzione Media', 'Produzione Ottimale'],
        'Produzione (kg/m²)': [
            produzione_simulata,
            benchmark['Sfavorevole'],
            benchmark['Media'],
            benchmark['Ottimale']
        ]
    }

    # 4. Creazione del DataFrame
    df_plot = pd.DataFrame(data_to_plot)

    # Return del DataFrame e del valore numerico
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
