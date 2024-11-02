import streamlit as st
import pandas as pd
import numpy as np

st.title("Recherchez une action")
action = st.text_input("Entrez le nom de l'action")

if action:
    st.write(f"Résultats pour : {action}")

    st.subheader("Indicateurs boursiers")
    st.metric(label="Prix actuel", value="$150.00", delta="+1.25%")
    st.metric(label="Variation sur 1 jour", value="+0.75%")
    st.metric(label="Volume moyen (10 jours)", value="1.2M")

    data = {
        "Date": pd.date_range(start="2024-01-01", periods=10, freq="D"),
        "Prix de clôture": np.random.uniform(140, 160, 10),
        "Volume": np.random.randint(100000, 500000, 10),
    }
    df = pd.DataFrame(data)

    st.subheader("Historique des prix et du volume")
    st.dataframe(df)

    st.subheader("Graphique des prix de clôture")
    st.line_chart(df.set_index("Date")["Prix de clôture"])
