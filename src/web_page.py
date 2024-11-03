import streamlit as st
import pandas as pd
import yfinance as yf
from data_request import write_financial_report
from json_claude import analyze_json

st.title("Recherchez une action")
action = st.text_input("Entrez le nom de l'action")

if action:
    ticker = yf.Ticker(action)
    company_info = ticker.info

    st.write(f"Résultats pour : {action}")
    st.write(f"Entreprise : {company_info.get('shortName', 'Nom indisponible')}")
    description = company_info.get('longBusinessSummary', 'Description indisponible')
    st.write("Description :")

    # Créer un espace réservé pour la description
    description_placeholder = st.empty()

    # Afficher la description courte par défaut
    if len(description) > 300:
        short_description = description[:300] + "..."
    else:
        short_description = description

    # Afficher la description dans l'espace réservé
    description_placeholder.write(short_description)

    # Placer la case à cocher en dessous de la description
    show_full_description = st.checkbox("Voir plus")

    # Mettre à jour la description si la case est cochée
    if show_full_description:
        description_placeholder.write(description)

    history = ticker.history(period="1y")
    st.subheader("Historique des prix et du volume")

    # Créer deux colonnes pour le tableau et le graphique
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Tableau des prix de clôture et du volume**")
        st.dataframe(history[['Close', 'Volume']])

    with col2:
        st.write("**Graphique des prix de clôture**")
        st.line_chart(history['Close'])

    write_financial_report(action)
    st.subheader("Analyse de Claude :")
    response = analyze_json(f'{action}_AnnualFinancialReport.json')
    st.write(response)
