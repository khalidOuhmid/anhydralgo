import matplotlib.pyplot as plt
import pandas as pd
import pymssql
import argparse
import numpy as np

# connexion à la base SAE_TEAM5
psw = 'fqnsbtc4'
usr = 'etd05'
dtbs = 'SAE_TEAM5'
cnxn = pymssql.connect ( server = 'info-mssql-etd', user = usr,      
                        password = psw, database = dtbs ) 
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

    # data
    cursor.execute(theCommand)

    # Récupération des données dans un DataFrame
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=[legendeX, legendeY])

    # Convertir les données de l'axe y en numérique, en forçant les erreurs à NaN (Not a Number)
    df[legendeY] = pd.to_numeric(df[legendeY], errors='coerce')

    # Supprimer les lignes avec des valeurs NaN dans les données de l'axe y
    df = df.dropna(subset=[legendeY])

    # Créer le graphique
    plt.figure(figsize=(12, 6))

    # Création du graphique
    if 'LINE view' in graphName:
        plt.plot(df[legendeX], df[legendeY])
    """
    elif 'BAR view' in graphName:
        plt.bar(df[legendeX], df[legendeY])
    elif 'PIE view' in graphName:
        plt.pie(df[legendeY], labels=df[legendeX], autopct='%1.1f%%', startangle=140)
    elif 'HISTOGRAM view' in graphName:
        plt.hist(df[legendeY])
    else:
        plt.plot(df[legendeX], df[legendeY])
    """
    #plt.plot(df[legendeX], df[legendeY])
    plt.title(graphName)
    plt.xlabel(legendeX)
    plt.ylabel(legendeY)
    plt.grid(True)
    
    # Calculer les ticks pour l'axe des ordonnées
    y_min, y_max = df[legendeY].min(), df[legendeY].max()
    y_ticks = np.linspace(y_min, y_max, 5)
    plt.yticks(y_ticks, fontsize=10)

    # Sauvegarde du graphique dans un fichier
    plt.savefig('../../pictures/' + graphName + '.png')
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