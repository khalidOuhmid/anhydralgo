import matplotlib.pyplot as plt
import pandas as pd
import pymssql
import argparse
import numpy as np

# Connexion à la base SAE_TEAM5
psw = 'fqnsbtc4'
usr = 'etd05'
dtbs = 'SAE_TEAM5'
cnxn = pymssql.connect(server='info-mssql-etd', user=usr,
                       password=psw, database=dtbs)
cursor = cnxn.cursor()

print('<- connected! ->')

"""
Comment cela fonctionne ?
Pour appeler la méthode, il faut deux éléments :
    - la commande, construite dans le C# (perm)
    - le nom du graphe pour son enregistrement

Le format attendu des commandes est le suivant : 
SELECT <valeur_abscisse>, <valeur_ordonnée>
"""
def getPicture(theCommand, legendeX, legendeY, graphName):

    # Exécuter la commande SQL
    cursor.execute(theCommand)
    rows = cursor.fetchall()
    
    # Convertir les données récupérées en DataFrame pandas
    df = pd.DataFrame(rows, columns=['DTA_VALEUR', 'EGY_NOM', 'PYS_NOM', 'DAT_DATE'])

    # Convertir DTA_VALEUR en numérique, forcer les erreurs à NaN puis les supprimer
    df['DTA_VALEUR'] = pd.to_numeric(df['DTA_VALEUR'], errors='coerce')
    df.dropna(subset=['DTA_VALEUR'], inplace=True)

    # Agréger les valeurs par nom d'activité
    aggregated_data = df.groupby('EGY_NOM')['DTA_VALEUR'].sum()

    # Créer un graphique en secteurs
    plt.figure(figsize=(10, 7))
    wedges, _, autotexts = plt.pie(aggregated_data, labels=None, autopct='%1.1f%%', startangle=140)

    # Ajouter une légende avec un meilleur positionnement
    plt.legend(wedges, aggregated_data.index, title="Activities", loc="center left", bbox_to_anchor=(1, 0.5), fontsize='small')
    plt.title(graphName) # TO DO
    plt.axis('equal')  # Un rapport d'aspect égal assure que le graphique en secteurs est circulaire.

    # Ajuster la disposition pour faire de la place pour la légende
    plt.tight_layout()

    # Sauvegarde du graphique dans un fichier
    plt.savefig('../../pictures/' + graphName + '.png') # /// ATTENTION \\\ LE CHEMIN EST RELATIF A L'APPLICATION QUI EXECUTE LE SCRIPT
    plt.close()

    return

if __name__ == '__main__':
    # Gestion des arguments
    parser = argparse.ArgumentParser(description='Générer un graphique à partir de la base de données.')
    parser.add_argument('theCommand', type=str, help='La commande SQL à exécuter')
    parser.add_argument('legendeX', type=str, help='Légende de l\'axe X')
    parser.add_argument('legendeY', type=str, help='Légende de l\'axe Y')
    parser.add_argument('graphName', type=str, help='Nom du fichier du graphique')

    args = parser.parse_args()

    # Appel de la méthode getPicture avec les arguments fournis
    getPicture(args.theCommand, args.legendeX, args.legendeY, args.graphName)