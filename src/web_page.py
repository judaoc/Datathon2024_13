import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import re

from data_fetch import getFinancialReport, getTrendy
from news_request import getNews, getSpecificNews
from json_claude import analyze_json_data
from data_fetch import get_rsi, get_macd, get_obv

st.title("Recherchez une action")
action = st.text_input("Entrez le nom de l'action")

if action:
    try:
        ticker = yf.Ticker(action)
        company_info = ticker.info

        if "symbol" not in company_info or company_info.get('symbol') is None:
            st.subheader("Ticker invalide, veuillez réessayer.")
        else:
            with st.expander(f"Entreprise : {company_info.get('shortName', 'Nom indisponible')}"):
                description = company_info.get('longBusinessSummary', 'Description indisponible')
                
                description_placeholder = st.empty()
                short_description = description[:300] + "..." if len(description) > 300 else description
                description_placeholder.write(short_description)

                show_full_description = st.checkbox("Voir plus")
                if show_full_description:
                    description_placeholder.write(description)

            with st.expander("Principaux actionnaires"):
                try:
                    holders = ticker.institutional_holders
                    if holders is not None and not holders.empty:
                        st.write("Voici les principaux actionnaires institutionnels :")
                        for index, row in holders.iterrows():
                            holder_name = row.get('Holder', 'Nom indisponible')
                            holder_percentage = row.get('pctHeld', 0) * 100
                            st.write(f"- {holder_name}: {holder_percentage:.4f}%")
                    else:
                        st.write("Informations sur les principaux actionnaires non disponibles.")
                except Exception as e:
                    st.write("Erreur lors de la récupération des actionnaires :", e)

            with st.expander("Principaux indices financiers"):
                rsi = get_rsi(action)
                macd = get_macd(action)
                obv = get_obv(action)

                st.write(f"RSI (14 jours): {rsi.iloc[-1]:.2f}")
                st.write(f"MACD: {macd['MACD_12_26_9'].iloc[-1]:.2f}")
                st.write(f"Ligne de signal MACD: {macd['MACDs_12_26_9'].iloc[-1]:.2f}")
                st.write(f"OBV: {obv.iloc[-1]:.2f}")
                peg_ratio = company_info.get('pegRatio', 'Non disponible')
                st.write(f"PEG Ratio : {peg_ratio}")

                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(x=rsi.index, y=rsi, mode='lines', name='RSI'))
                fig_rsi.update_layout(title="RSI (14 jours)", xaxis_title="Date", yaxis_title="RSI")
                st.plotly_chart(fig_rsi)

                fig_macd = go.Figure()
                fig_macd.add_trace(go.Scatter(x=macd.index, y=macd['MACD_12_26_9'], mode='lines', name='MACD'))
                fig_macd.add_trace(go.Scatter(x=macd.index, y=macd['MACDs_12_26_9'], mode='lines', name='Signal Line'))
                fig_macd.update_layout(title="MACD et ligne de signal", xaxis_title="Date", yaxis_title="MACD")
                st.plotly_chart(fig_macd)

                fig_obv = go.Figure()
                fig_obv.add_trace(go.Scatter(x=obv.index, y=obv, mode='lines', name='OBV'))
                fig_obv.update_layout(title="OBV (On-Balance Volume)", xaxis_title="Date", yaxis_title="OBV")
                st.plotly_chart(fig_obv)

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
                    y=history['Volume'] / 1_000_000,
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

            def cleanTitle(article_text):
                cleaned_text = re.sub(r'\s+', ' ', article_text.replace('\n', ' '))
                return cleaned_text
                
            with st.expander("Articles pertinents :"):
                news_placeholder = st.empty()
                news_placeholder.write("Accès à l'actualité...")
                news = getSpecificNews("ffa0ad83fa8c4d87bef0c77c3fe41eeb", company_info.get('symbol'))
                news_placeholder.empty()
                articles_list = "\n".join([f"- [{cleanTitle(title).strip()}]({url})" for title, url in news])
                news_placeholder.markdown(articles_list)

            with st.expander("Analyse de Claude :"):
                analysis_placeholder = st.empty()
                analysis_placeholder.write("Analyse en cours...")

                financialReport = getFinancialReport(action)
                response = analyze_json_data(financialReport, action)
                analysis_placeholder.write(response)
                
    except Exception as e:
        st.subheader("Une erreur s'est produite lors de la récupération des données. Veuillez vérifier le ticker.")
        st.error(str(e))

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
