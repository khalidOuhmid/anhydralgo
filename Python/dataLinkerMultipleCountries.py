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
    
    # Récupérer les données et créer un DataFrame
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['Date', 'Pays', legendeY])
    
    # Convertir les données de l'axe y en numérique, en forçant les erreurs à NaN (Not a Number)
    df[legendeY] = pd.to_numeric(df[legendeY], errors='coerce')
    
    # Supprimer les lignes avec des valeurs NaN dans les données de l'axe y
    df = df.dropna(subset=[legendeY])
    
    # Créer le graphique
    plt.figure(figsize=(12, 6))
    
    # Tracer chaque pays séparément
    for pays in df['Pays'].unique():
        df_pays = df[df['Pays'] == pays]
        plt.plot(df_pays['Date'], df_pays[legendeY], label=pays)
    
    plt.title(graphName)
    plt.xlabel(legendeX)
    plt.ylabel(legendeY)
    plt.grid(True)
    plt.legend()
    
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