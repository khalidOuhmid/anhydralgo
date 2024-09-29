import pandas as pd
import pyodbc
import pycountry
import pycountry_convert as pc

# Détails de connexion
server = 'INFO-MSSQL-ETD'
database = 'SAE_TEAM5'
username = 'etd05'
password = 'fqnsbtc4'
fichiers = [
    'Z:/Documents/saeTruc/combined_temperature.csv',
]

continents = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe',
    'WW': 'World'
}
cont = ['North America','South America','Asia','Australia','Africa','Europe','World','Caribbean'
,'demographic','Euro','conflict','poor','income','IBRD','IDA','countries','OECD','small','Small','Bahamas','Channel','Dem','Rep','Curacao','Hong']

def get_Region(country_name):
    try:
        country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
        continent_name = pc.country_alpha2_to_continent_code(country_code)
        return continents[continent_name]
    except KeyError as e:
        print(f"KeyError encountered: {str(e)}")
        return country_name
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return country_name

def get_region_and_country(entity):
    """Extrait le nom de la région et du pays à partir du nom de l'entité."""
    region_name = entity
    country_name = entity
    if(region_name == "Cote d'Ivoire"):
        country_name = 'Ivory Coast'
    if(region_name == 'Gambia, The'):
        country_name = 'Gambia'

    for continent in cont:
        if continent in region_name:
            return region_name, country_name
    else:
        region_name = get_Region(country_name)
        return region_name, country_name

def process_row(entity, code, year, value, conn):
    region_name, country_name = get_region_and_country(entity)

    unit = '(°C)'

    try:
        year = int(year)
        if year < 1950 or year > 3000:
            raise ValueError(f"Année invalide : {year}")
        date_string = f"{year}-01-01"
    except ValueError as e:
        print(f"Erreur de conversion de l'année : {e}")
        return

    with conn.cursor() as cursor:
        if region_name:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM T_REGION_REG WHERE REG_NOM = ?)
                BEGIN
                    INSERT INTO T_REGION_REG (REG_NOM) VALUES (?)
                END
            """, region_name, region_name)
            conn.commit()

            cursor.execute("SELECT REG_ID FROM T_REGION_REG WHERE REG_NOM = ?", region_name)
            row = cursor.fetchone()
            if row:
                region_id = row[0]
            else:
                region_id = None
        else:
            region_id = None

        if country_name:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM T_PAYS_PYS WHERE PYS_NOM = ?)
                BEGIN
                    INSERT INTO T_PAYS_PYS (REG_ID, PYS_NOM) VALUES (?, ?)
                END
            """, country_name, region_id, country_name)
            conn.commit()

            cursor.execute("SELECT PYS_ID FROM T_PAYS_PYS WHERE PYS_NOM = ?", country_name)
            row = cursor.fetchone()
            if row:
                country_id = row[0]
            else:
                country_id = None
        else:
            country_id = None

        if country_id:
            # Insérer la date si elle n'existe pas déjà
            try:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM T_DATE_DAT WHERE DAT_DATE = ?)
                    BEGIN
                        INSERT INTO T_DATE_DAT (DAT_DATE) VALUES (?)
                    END
                """, date_string, date_string)
                conn.commit()
            except pyodbc.DataError as e:
                print(f"Erreur de conversion de date pour l'année {year}: {e}")
                return

            # Récupérer l'ID de la date
            cursor.execute("SELECT DAT_ID FROM T_DATE_DAT WHERE DAT_DATE = ?", date_string)
            row = cursor.fetchone()
            if row:
                date_id = row[0]
            else:
                date_id = None

            if date_id:
                cursor.execute("""
                    INSERT INTO T_DATA_DTA (PYS_ID, DAT_ID, DTA_VALEUR, DTA_NOM, DTA_UNITE)
                    VALUES (?, ?, ?, ?, ?)
                """, country_id, date_id, value, "Annual Temperature", unit)
                conn.commit()

def process_file(filename, conn):
    df = pd.read_csv(filename, delimiter=',', names=['Country', 'Year', 'Annual Mean', '5-yr smooth', 'Code'], skiprows=1)
    
    for index, row in df.iterrows():
        try:
            year = int(row['Year'])
            if year >= 1950:
                value = float(row['Annual Mean'])
                process_row(row['Country'], row['Code'], row['Year'], value, conn)
            else:
                print(f"Donnée ignorée pour l'année {year} (avant 1950)")
        except ValueError:
            print(f"Valeur non numérique ou année invalide pour la ligne {index}: {row}")

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
    print("Erreur de connexion : ", e)
    exit()

# Traitement des fichiers
for fichier in fichiers:
    process_file(fichier, conn)

conn.close()
