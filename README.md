# Datathon de Polyfinance 2024 (Équipe 13)

## Authors

- [@judaoc](https://github.com/judaoc)
- [@guillaumestpierre](https://github.com/guillaumestpierre)
- [@charlo3112](https://github.com/charlo3112)
- [@GuilhemDM](https://github.com/GuilhemDM)


## Créé pour

Ce projet a été créé pour le Datathon 2024 de PolyFinance

## Description
Notre projet est capable de faire des résumés automatiques des rapports financiers en choisissant les mots clés. Il permet d'aider les analystes financiers en lui donnant les valeurs des actions les plus actives de la journée. Cela lui permet de rester au courant des mouvements dans le marché tout en consultant nos autres outils d'analyse. De plus, nous avons créé un outil utilisant l'IA générative. Il a été conçu avec des données d'inflation de plusieurs années, des données sur le taux d'intérêt. Nous lui avons aussi donné des données sur différentes compagnies du marché. Dans notre cas, nous avons seulement quelques compagnies, dont les plus grandes compagnies du secteur technologique. Les informations que nous lui avons données sont les informations sur les symboles, les historiques de leurs données depuis les 5 dernières années, les données financières comme le "Balance Sheet", le "Income Statement" et le "Cash Flow Statement". Grâce à cette base de données, qui est située dans S3, il est capable de générer des analyses futures sur les historiques des données de l'action, mais aussi sur les différentes données d'inflation et de taux d'intérêt. Lorsque l'analyste entre sur le site web, il est possible pour lui de consulter différents graphiques dont: le graphique de l'action ainsi que des différents indices comme RSI, MACD et OBV. Il est aussi possible pour l'analyste d'avoir des suggestions d'articles par rapport à l'action qu'il est en train de consulter. De plus, l'outil d'IA générative permet de donner une certaine analyse du stock et son sentiment général basé sur les différentes données qu'il a récoltées sur l'action. Enfin, notre interface permet aussi à l'analyste de consulter les principaux actionnaires liés à l'action recherchée.


## Dépendances
Voici les dépendances qu'il faut avoir pour rouler le programme localement


-Vous devez utiliser la version de numpy 1.26.4 
 `pip install --force-reinstall numpy==1.26.4`

-`pip install pandas pandas_ta yfinance yahoo_fin streamlit python-dotenv plotly lxml[html_clean] requests_html boto3 uuid`


## Run le programme localement
Vous devez être dans le dossier `src`

**Il faut avoir des credentials valides AWS qu'il faut entrer dans la console dans la racine du projet**

`streamlit run web_page.py`

