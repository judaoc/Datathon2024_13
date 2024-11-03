import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

from data_request import getFinancialReport, getTrendy, getNews
from json_claude import analyze_json_data

st.title("Recherchez une action")
action = st.text_input("Entrez le nom de l'action")

if action:
    ticker = yf.Ticker(action)
    company_info = ticker.info

    # Collapsible section for company information
    with st.expander(f"Entreprise : {company_info.get('shortName', 'Nom indisponible')}"):
        description = company_info.get('longBusinessSummary', 'Description indisponible')
        
        description_placeholder = st.empty()
        if len(description) > 300:
            short_description = description[:300] + "..."
        else:
            short_description = description

        description_placeholder.write(short_description)

        show_full_description = st.checkbox("Voir plus")
        if show_full_description:
            description_placeholder.write(description)

    # Collapsible section for interactive price and volume chart
    with st.expander("Graphique interactif des prix de clôture et du volume"):
        periode = st.selectbox(
            "Sélectionnez une période pour afficher les données :",
            options=["1 mois", "3 mois", "6 mois", "1 an", "5 ans", "10 ans"]
        )

        periode_mapping = {
            "1 mois": "1mo",
            "3 mois": "3mo",
            "6 mois": "6mo",
            "1 an": "1y",
            "5 ans": "5y",
            "10 ans": "10y"
        }

        selected_period = periode_mapping[periode]
        history = ticker.history(period=selected_period)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=history.index,
            y=history['Close'],
            mode='lines',
            name='Prix de clôture',
            line=dict(color='lightblue'),
            yaxis="y1"
        ))

        fig.add_trace(go.Bar(
            x=history.index,
            y=history['Volume'] / 1_000_000,  # Conversion en millions
            name='Volume (en millions)',
            marker=dict(color='gray', opacity=0.3),
            yaxis="y2"
        ))

        fig.update_layout(
            title="Historique des prix de clôture et du volume",
            xaxis=dict(title="Date"),
            yaxis=dict(
                title="Prix de clôture",
                titlefont=dict(color="gray"),
                tickfont=dict(color="gray"),
                side="left"
            ),
            yaxis2=dict(
                title="Volume (en millions)",
                titlefont=dict(color="gray"),
                tickfont=dict(color="gray"),
                overlaying="y",
                side="right"
            ),
            legend=dict(x=0, y=1.2)
        )

        st.plotly_chart(fig)

    # Collapsible section for financial report analysis
    with st.expander("Analyse de Claude :"):
        analysis_placeholder = st.empty()
        analysis_placeholder.write("Analyse en cours...")

        financialReport = getFinancialReport(action)
        response = analyze_json_data(financialReport, action)
        analysis_placeholder.write(response)

with st.sidebar:
    st.title("À la une !")
    trendy = getTrendy()

    for index, row in trendy.iterrows():
        stock_name = row['Symbol']
        price_change = row['Price']
        price_change_value = float(price_change.split()[1])
        color = 'green' if price_change_value > 0 else 'red'
        st.markdown(f"{stock_name}: <span style='color:{color};'>{price_change}</span>", unsafe_allow_html=True)

    st.title("Articles")
    news = getNews("ffa0ad83fa8c4d87bef0c77c3fe41eeb")
    for title, url in news:
        st.sidebar.markdown(f"[{title}]({url})")
