# MarketIntelAI

## Authors

- [@judaoc](https://github.com/judaoc)
- [@guillaumestpierre](https://github.com/guillaumestpierre)
- [@charlo3112](https://github.com/charlo3112)
- [@GuilhemDM](https://github.com/GuilhemDM)


## Créé pour

Ce projet a été créé pour le Datathon 2024 de PolyFinance (Équipe 13)

## Problème abordé 
Les analystes financiers doivent manipuler avec des volumes massifs de données pour suivre les actions les plus actives et les nouvelles les plus importantes, analyser les tendances historiques et interpréter les impacts économiques de l’inflation et du taux d’intérêt. Cette surcharge de données rend difficile une prise de décision rapide et éclairée.

## Description de la solution 
MarketIntelAI automatise la synthèse des rapports financiers et analyse les tendances du marché pour fournir une vision claire et structurée des actions et des indicateurs économiques. 

## Fonctionnalités clés
-	**Résumé automatique des rapports financiers** : Génère des résumés clairs des documents financiers essentiels pour une analyse rapide.
-	**Suivi des actions actives** : Affiche les valeurs des actions les plus actives en temps réel.
-	**Analyses historiques et prédictives** : Utilise les données d’inflation, taux d’intérêt et historiques de compagnies pour prédire des tendances futures.
-	**Visualisation des graphiques financiers** : Présente des graphiques personnalisés (RSI, MACD, OBV) pour chaque action.
-	**Suggestions d’articles en lien avec les actions** : Propose des articles en fonction de l’action consultée, pour enrichir la compréhension de l’analyste.
-	**Accès aux informations des principaux actionnaires** : Visualise les investisseurs clés pour une meilleure contextualisation.

## Technologies et ressources utilisées 
-	**Technologie AWS** : BedRock (modèle d’IA spécialisé en analyse d’effets des taux d’intérêts et d’inflation sur la valeur des stocks), S3 (stockage des données financières et historiques), Lambda ( permets la recherche d’informations pertinentes dans S3)
-	**Sources de données** : Yahoo Finance (pour les données sur les infos des stocks, les nouvelles, les données historiques, les données du « Balance Sheet », le « Income Statement » et le « Cash Flow Statement »), US. Federal funds rate (les données sur le taux d’intérêt => https://www.statista.com/statistics/187616/effective-rate-of-us-federal-funds-monthly/) et FRED ( pour les données historiques de l’inflation => https://fred.stlouisfed.org/series/FPCPITOTLZGUSA)

## Dépendances
Voici les dépendances qu'il faut avoir pour rouler le programme localement


-Vous devez utiliser la version de numpy 1.26.4 `pip install --force-reinstall numpy==1.26.4`

-`pip install pandas pandas_ta yfinance yahoo_fin streamlit python-dotenv plotly lxml[html_clean] requests_html boto3 uuid`


## Exécuter le programme localement
Vous devez être dans le dossier `src`

**Il faut avoir des credentials valides AWS qu'il faut entrer dans la console dans la racine du projet**

`streamlit run web_page.py`

## Démonstration

