from Funnspredning_funksjoner import (
    generer_tilfeldige_punkter,
    velg_fil,
    oppdater_dataframe_med_nye_tall,
    les_inn_csv_og_filtrer
)

# La brukeren velge en fil
filnavn = velg_fil()

# Sjekk om en fil ble valgt før du fortsetter
if filnavn:
    # Les inn CSV-filen som en DataFrame
    df = les_inn_csv_og_filtrer(filnavn)

    # Sjekk om DataFrame ble opprettet før du fortsetter
    if df is not None:
        # Bruk funksjonen på din dataframe
        df = generer_tilfeldige_punkter(df)

        # Gjør hva du vil med den oppdaterte dataframe
        print(df)
else:
    print("Ingen fil ble valgt.")