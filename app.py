# Auteur : Joelle GERMANOS
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import urllib.request


données = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

# 5. Création de la colonne Chiffre d'Affaires
données['CA'] = données['prix'] * données['qte']
# a. Chiffre d’affaires par produit et Volume des ventes par produit
# i. Moyenne
moyennes = données.groupby('produit')[['CA', 'qte']].mean().round(2)
print("MOYENNES :\n", moyennes)
# ii. Médiane
médianes = données.groupby('produit')[['CA', 'qte']].median().round(2)
print("\nMÉDIANES :\n", médianes)
# b. Volume des ventes (qte) par produit 
# i. Écart-type
ecart_type = données.groupby('produit')['qte'].std().round(2)
print("\nÉCART-TYPE (Volume) :\n", ecart_type)
# ii. Variance
variance = données.groupby('produit')['qte'].var().round(2)
print("\nVARIANCE (Volume) :\n", variance)



# 6. Créer du code qui permet de trouver le produit le plus vendu et le moins vendu en nombre d’unités vendues.
url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv"

# Téléchargement des données
response = urllib.request.urlopen(url_csv)
lignes = response.read().decode('utf-8').splitlines()
cumul_ventes = {}

# On commence à la ligne 1 pour sauter l'en-tête
for i in range(1, len(lignes)):
    colonnes = lignes[i].split(',')
    nom_produit = colonnes[1] # Colonne 'produit'
    quantite = int(colonnes[3]) # Colonne 'qte' (conversion en entier)
    # On ajoute la quantité au produit existant ou on initialise à 0
    cumul_ventes[nom_produit] = cumul_ventes.get(nom_produit, 0) + quantite

produit_max = max(cumul_ventes, key=cumul_ventes.get)
produit_min = min(cumul_ventes, key=cumul_ventes.get)

#print(f"Plus vendu : {produit_max} | Moins vendu : {produit_min}")
print(f"Produit le plus vendu : {produit_max} ({cumul_ventes[produit_max]} unités)")
print(f"Produit le moins vendu : {produit_min} ({cumul_ventes[produit_min]} unités)")

# 7. Graphiques
stats = données.groupby('produit').agg({'qte': 'sum', 'CA': 'sum'}).reset_index()

# Création des deux graphiques avec Plotly Express
fig1 = px.bar(stats, x='produit', y='qte', title="Les Ventes par Produit")
fig2 = px.bar(stats, x='produit', y='CA', title="Le Chiffre d'Affaires par Produit")

# Pour les mettre côte à côte dans une seule figure HTML
# On crée une structure vide
final_fig = make_subplots(rows=1, cols=2, subplot_titles=("Les Ventes par Produit", "Le Chiffre d'Affaires par Produit"))

# On ajoute les "traces" (le contenu) des graphiques px dans la structure
for trace in fig1.data:
    final_fig.add_trace(trace, row=1, col=1)

for trace in fig2.data:
    final_fig.add_trace(trace, row=1, col=2)

# Mise à jour du design et EXPORT HTML
final_fig.update_layout(height=500, title_text="Tableau de Bord des Ventes", showlegend=False)

# Génération du fichier HTML
final_fig.write_html("analyse_ventes_express.html")

print("Fichier 'analyse_ventes_express.html' généré !")





#figure = px.pie(données, values='qte', names='region', title='quantité vendue par région')
#figure.write_html('ventes-par-region.html')
#print('ventes-par-région.html généré avec succès !')
