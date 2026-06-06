import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Cellule de Recrutement Data-Driven",
    page_icon="soccer",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("dataset_final_scouting_attaquants.csv")
    
    if 'target' not in df.columns:
        df['is_gem'] = np.where(
            (df['age'] <= 23) & (df['potential'] >= 75) & (df['market_value_in_eur'] <= 8000000),
            "Pepite Detectee", "Profil Standard"
        )
    else:
        df['is_gem'] = df['target'].map({1: "Pepite Detectee", 0: "Profil Standard"})
        
    return df

df = load_data()

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/5323/5323814.png", width=100)
st.sidebar.title("Filtres du Mercato")

budget_max = st.sidebar.slider(
    "Budget Maximum (EUR)", 
    min_value=500000, 
    max_value=30000000, 
    value=12000000, 
    step=500000
)

age_max = st.sidebar.slider("Age Maximum", 16, 40, 23)
overall_min = st.sidebar.slider("Note Globale Minimum (Overall)", 50, 99, 70)

df_filtered = df[
    (df['market_value_in_eur'] <= budget_max) & 
    (df['age'] <= age_max) & 
    (df['overall'] >= overall_min)
]

st.title("Systeme d'Aide a la Decision : Scouting IA")
st.subheader("Optimisation du recrutement de la ligne d'attaque")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Joueurs Correspondants", len(df_filtered))
with col2:
    pepites_trouvees = len(df_filtered[df_filtered['is_gem'] == "Pepite Detectee"])
    st.metric("Pepites IA Identifiees", pepites_trouvees)
with col3:
    if len(df_filtered) > 0:
        prix_moyen = df_filtered['market_value_in_eur'].mean()
        st.metric("Cout Moyen du Profil", f"{prix_moyen:,.0f} EUR")
    else:
        st.metric("Cout Moyen du Profil", "0 EUR")

st.markdown("---")

st.write("### Liste des recrues potentielles filtrees")
columns_to_show = ['long_name', 'age', 'overall', 'potential', 'market_value_in_eur', 'is_gem']

if not df_filtered.empty:
    st.dataframe(
        df_filtered[columns_to_show].sort_values(by='potential', ascending=False),
        use_container_width=True
    )
else:
    st.warning("Aucun joueur ne correspond a vos criteres budgetaires et sportifs actuels.")

st.markdown("---")

st.write("### Comparaison Detaillee (Moneyball)")

if not df_filtered.empty:
    liste_joueurs = df_filtered['long_name'].tolist()
    joueur_selectionne = st.selectbox("Selectionnez un joueur pour analyser son profil :", liste_joueurs)
    
    data_joueur = df_filtered[df_filtered['long_name'] == joueur_selectionne].iloc[0]
    
    categories = ['Overall', 'Potential', 'Vitesse (Simule)', 'Tir (Simule)', 'Dribble (Simule)']
    
    valeurs_joueur = [
        data_joueur['overall'], 
        data_joueur['potential'],
        75, 
        78, 
        72 
    ]
    
    valeurs_ancienne_star = [84, 86, 85, 83, 82]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valeurs_ancienne_star,
        theta=categories,
        fill='toself',
        name='Ancienne Star (Vendu - Ref)',
        line_color='red'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=valeurs_joueur,
        theta=categories,
        fill='toself',
        name=f"Recrue : {joueur_selectionne}",
        line_color='blue'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        title=f"Comparaison des competences : {joueur_selectionne} vs Profil recherche"
    )
    
    st.plotly_chart(fig, use_container_width=True)