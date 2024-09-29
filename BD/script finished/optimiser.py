import pandas as pd

def gas():
    # fichier CSV
    df = pd.read_csv('Z:\\Documents\\saeTruc\\edgar_processed_ch4_n2o_co2_fgasesTranslated.csv')

    # Filtrer les années avant 1990
    df = df[df['year'] >= 1990]

    # Supprimer les lignes avec des valeurs vides ou égales à 0 dans les colonnes 'value_kt' et 'value_mteqco2'
    df = df.dropna(subset=['value_kt', 'value_mteqco2'])
    df = df[(df['value_kt'] != 0) & (df['value_mteqco2'] != 0)]

    # Sauvegarder dans un nouveau fichier CSV
    df.to_csv('Z:\\Documents\\saeTruc\\edgar_processed_ch4_n2o_co2_fgasesTranslatedMieux.csv', index=False)

    print("Le fichier filtré a été sauvegardé sous le nom 'edgar_processed_ch4_n2o_co2_fgasesTranslatedMieux.csv'")

import pandas as pd

def energy():
    # fichier CSV
    df = pd.read_csv('Z:\\Documents\\saeTruc\\bp_file_energy_review_world.csv')

    # Filtrer les années avant 1990
    df = df[df['Year'] >= 1990]

    # Supprimer les lignes avec des valeurs vides ou égales à 0 dans la colonne 'Value'
    df = df.dropna(subset=['Value'])
    df = df[df['Value'] != 0]

    # Sauvegarder dans un nouveau fichier CSV
    df.to_csv('Z:\\Documents\\saeTruc\\bp_file_energy_review_worldMieux.csv', index=False)

    print("Le fichier filtré a été sauvegardé sous le nom 'bp_file_energy_review_worldMieux.csv'")

energy()
gas()
