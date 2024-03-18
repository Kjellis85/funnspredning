import pandas as pd
import random
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def generer_tilfeldige_punkter(df):
    # Splitter kolonnen med retninger til to nye kolonner
    df[['nordsor', 'ostvest']] = df['Kvadrant'].str.split()

    # Initialiserer lister for de nye koordinatene
    y_cm_list = []
    x_cm_list = []

    # Genererer tilfeldige koordinater basert på retningene
    for index, row in df.iterrows():
        if row['nordsor'] == 'N':
            y_cm = random.uniform(0.501, 0.999)
        elif row['nordsor'] == 'S':
            y_cm = random.uniform(0.001, 0.499)
        else:
            raise ValueError("Ugyldig verdi i nordsor kolonnen")

        if row['ostvest'] == 'Ø':
            x_cm = random.uniform(0.501, 0.999)
        elif row['ostvest'] == 'V':
            x_cm = random.uniform(0.001, 0.499)
        else:
            raise ValueError("Ugyldig verdi i ostvest kolonnen")

        y_cm_list.append(y_cm)
        x_cm_list.append(x_cm)

    # Legger til de nye koordinatene som kolonner i dataframe
    df['y_cm'] = y_cm_list
    df['x_cm'] = x_cm_list

    return df

def les_inn_csv_og_filtrer(filnavn):
    """
    Leser inn en CSV-fil, filtrerer ut rader med manglende informasjon i spesifikke kolonner,
    og returnerer en pandas DataFrame sammen med antall ignorerte rader.

    Args:
        filnavn (str): Stien til CSV-filen som skal leses inn.

    Returns:
        pd.DataFrame: Dataframe som inneholder data fra CSV-filen.
        int: Antall rader som ble ignorert på grunn av manglende informasjon.
    """
    try:
        df = pd.read_csv(filnavn, sep=';', dtype={'X': int, 'Y': int, 'Kvadrant': str})

        # Teller totalt antall rader før filtrering
        totalt_antall_rader = len(df)

        # Filtrer ut rader med manglende informasjon i 'X', 'Y', eller 'Kvadrant'
        df_filtrert = df.dropna(subset=['X', 'Y', 'Kvadrant'])

        # Teller antall rader etter filtrering
        antall_rader_etter_filtrering = len(df_filtrert)

        # Beregner antall ignorerte rader
        antall_ignorerte_rader = totalt_antall_rader - antall_rader_etter_filtrering

        return df_filtrert, antall_ignorerte_rader
    except FileNotFoundError:
        print(f"Feil: Filen '{filnavn}' ble ikke funnet.")
        return None, 0
    except Exception as e:
        print(f"En feil oppstod ved lesing av filen '{filnavn}': {e}")
        return None, 0
    # funksjon for å velge fil gjennom filutforsker

def velg_fil():
    """
    Lar brukeren velge en fil gjennom en filutforskerdialog.

    Returns:
        str: Stien til den valgte filen, eller None hvis ingen fil ble valgt.
    """
    # Vi bruker Tkinter sin filvelgerdialog
    Tk().withdraw()  # Vi vil ikke ha et fullt GUI, så vi trekker tilbake roten
    filnavn = askopenfilename()  # Viser filvelgerdialogen og returnerer valgt filsti
    return filnavn


def erstatte_siste_sifre(basenummer, nytt_endingstall):
    """
    Erstatter de siste sifrene i basenummeret med nytt_endingstall.

    Args:
        basenummer (int): Det større tallet hvor siste sifrene skal erstattes.
        nytt_endingstall (int): Tallet som skal settes inn på slutten av basenummeret.

    Returns:
        int: Det nye tallet med erstattede siste sifre.
    """
    # Konverterer begge tallene til strenger for å kunne manipulere dem
    basenummer_str = str(basenummer)
    nytt_endingstall_str = str(nytt_endingstall)

    # Beregner lengden på endingstallet
    endingstall_lengde = len(nytt_endingstall_str)

    # Erstatter de siste sifrene i basenummeret med det nye endingstallet
    nytt_tall_str = basenummer_str[:-endingstall_lengde] + nytt_endingstall_str

    # Konverterer tilbake til int og returnerer det nye tallet
    return int(nytt_tall_str)

def oppdater_dataframe_med_nye_tall(df, nord_basenummer, ost_basenummer):
    """
    Oppdaterer DataFrame ved å erstatte de siste sifrene i nord- og øst-basenummeret
    med tallene fra kolonnene 'Y' og 'X'.

    Args:
        df (pd.DataFrame): Dataframen som skal oppdateres.
        nord_basenummer (int): Det større tallet for 'Nord'.
        ost_basenummer (int): Det større tallet for 'Øst'.

    Returns:
        pd.DataFrame: Den oppdaterte dataframen.
    """
    df['Nord'] = df['Y'].apply(lambda y: erstatte_siste_sifre(nord_basenummer, y))
    df['Øst'] = df['X'].apply(lambda x: erstatte_siste_sifre(ost_basenummer, x))
    return df