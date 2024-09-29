import pandas as pd
import pyodbc
import time
import pycountry_convert as pc

# Détails de connexion
server = 'INFO-MSSQL-ETD'
database = 'SAE_TEAM55'
username = 'etd05'
password = 'fqnsbtc4'
filename = 'Z:\\Documents\\saeTruc\\csv\\share-elec-by-source.csv'

cont = ['North America','South America','Asia','Australia','Africa','Europe','World','Caribbean',
        'demographic','Euro','conflict','poor','income','IBRD','IDA','countries','OECD','small','Small',
        'Bahamas','Channel','Dem','Rep','Curacao','Hong']

# Dictionnaire des activités
activities = {
    'Coal - % electricity': 'Coal',
    'Gas - % electricity': 'Gas',
    'Hydro - % electricity': 'Hydro',
    'Solar - % electricity': 'Solar',
    'Wind - % electricity': 'Wind',
    'Oil - % electricity': 'Oil',
    'Nuclear - % electricity': 'Nuclear',
    'Other renewables excluding bioenergy - % electricity': 'Other renewables excluding bioenergy',
    'Bioenergy - % electricity': 'Bioenergy'
}


def get_region_and_country(filename):
    region_name = filename
    country_name = filename
    if region_name == "Cote d'Ivoire":
        country_name = 'Ivory Coast'
    if region_name == 'Gambia, The':
        country_name = 'Gambia'
    for continent in cont:
        if continent in region_name:
            return region_name, country_name
    else:
        return region_name, country_name
    
def should_process_row(value, year):
    """Vérifie si une ligne doit être traitée."""
    return pd.notna(value) and value != 0 and year > 1990

def get_or_create_date_id(cursor, year):
    date_str = f"{year}-01-01"
    cursor.execute("SELECT DAT_ID FROM T_DATE_DAT WHERE DAT_DATE = ?", date_str)
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO T_DATE_DAT (DAT_DATE) VALUES (?)", date_str)
        cursor.execute("SELECT DAT_ID FROM T_DATE_DAT WHERE DAT_DATE = ?", date_str)
        return cursor.fetchone()[0]

def process_chunk(df_chunk, conn, batch_size=100):
    cursor = conn.cursor()
    batch = []
    start_chunk_time = time.time()

    for index, row in df_chunk.iterrows():
        year = row['Year']
        region = row['Entity']
        for column, activity in activities.items():
            value = row[column]
            if should_process_row(value, year):
                try:
                    value = round(float(value), 6)
                except ValueError:
                    print(f"Valeur invalide pour '{column}' à la ligne {index}: {value}")
                    continue

                unit = '%'

                # Ajouter les données au batch
                batch.append((region, year, activity, value, unit))

                if len(batch) >= batch_size:
                    # Insérer le batch
                    insert_batch(batch, cursor)
                    batch = []

    # Insérer le dernier batch restant
    if batch:
        insert_batch(batch, cursor)

    conn.commit()
    end_chunk_time = time.time()
    print(f"Temps de traitement du chunk: {end_chunk_time - start_chunk_time:.2f} secondes")

def insert_batch(batch, cursor):
    
    for data in batch:
        region, year, activity, value, unit = data

        try:
            region, country_name = get_region_and_country(region)
            if region:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_REGION_REG WHERE REG_NOM = ?)
                    BEGIN
                        INSERT INTO T_REGION_REG (REG_NOM) VALUES (?)
                    END
                """, region, region)
                cursor.execute("SELECT REG_ID FROM T_REGION_REG WHERE REG_NOM = ?", region)
                region_id = cursor.fetchone()[0]
            else:
                region_id = None

            # Vérifier et insérer les pays
            if country_name:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_PAYS_PYS WHERE PYS_NOM = ?)
                    BEGIN
                        INSERT INTO T_PAYS_PYS (REG_ID, PYS_NOM) VALUES (?, ?)
                    END
                """, country_name, region_id, country_name)
                cursor.execute("SELECT PYS_ID FROM T_PAYS_PYS WHERE PYS_NOM = ?", country_name)
                country_id = cursor.fetchone()[0]
            else:
                country_id = None

            # Vérifier et insérer les activités
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM T_ENERGY_EGY WHERE EGY_NOM = ?)
                BEGIN
                    INSERT INTO T_ENERGY_EGY (EGY_NOM) VALUES (?)
                END
            """, (activity, activity))
            cursor.execute("SELECT EGY_ID FROM T_ENERGY_EGY WHERE EGY_NOM = ?", (activity,))
            EGY_ID = cursor.fetchone()[0]

            # Obtenir ou créer DAT_ID
            date_id = get_or_create_date_id(cursor, year)

            # Insérer les données
            cursor.execute("""
                INSERT INTO T_DATA_DTA (PYS_ID, DAT_ID, EGY_ID, DTA_VALEUR, DTA_NOM, DTA_UNITE)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (country_id, date_id, EGY_ID, value, activity, unit))
        except pyodbc.Error as e:
            print(f"Erreur lors de l'insertion des données : {e}")

def process_file(filename, conn, chunksize=1000):
    total_chunks = 0
    try:
        for chunk in pd.read_csv(filename, chunksize=chunksize):
            process_chunk(chunk, conn)
            total_chunks += 1
    except pd.errors.EmptyDataError:
        print("Le fichier est vide.")
    except pd.errors.ParserError as e:
        print(f"Erreur de lecture du fichier CSV : {e}")

    print(f"Nombre total de chunks traités: {total_chunks}")

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    print("Connexion réussie à la base de données")
except pyodbc.Error as e:
    print(f"Erreur de connexion : {e}")
    exit()

# Mesure du temps de traitement
start_time = time.time()

# Traitement des fichiers
process_file(filename, conn)

end_time = time.time()

print('finished')
print(f"Temps total utilisé : {end_time - start_time:.2f} secondes")
conn.close()
