from html import escape
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Scouting Data-Driven",
    page_icon=":soccer:",
    layout="wide",
)


DATA_FILE = Path(__file__).resolve().parent / "dataset_final_scouting_attaquants.csv"
ACCENT = "#1f7a5c"
CARD_BG = "#ffffff"
PANEL_BG = "#f4f7f3"
TEXT_MUTED = "#607067"
LINE = "rgba(31, 122, 92, 0.16)"


def format_currency(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f} M EUR"
    if value >= 1_000:
        return f"{value / 1_000:.0f} K EUR"
    return f"{value:,.0f} EUR"


def format_score(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.1f}"


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset introuvable: {DATA_FILE.name}. Genere-le depuis dataprep.ipynb."
        )

    df = pd.read_csv(DATA_FILE)

    if "target" not in df.columns:
        df["is_gem"] = np.where(
            (df["age"] <= 23)
            & (df["potential"] >= 75)
            & (df["market_value_in_eur"] <= 8_000_000),
            "Pepite detectee",
            "Profil standard",
        )
    else:
        df["is_gem"] = df["target"].map({1: "Pepite detectee", 0: "Profil standard"})

    df["market_value_m"] = df["market_value_in_eur"] / 1_000_000
    df["gap_to_potential"] = df["potential"] - df["overall"]
    df["value_index"] = (
        (df["potential"] * 1.35 + df["overall"] * 1.0 + df["pace"].fillna(0) * 0.35)
        / df["market_value_m"].replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan)

    return df


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background:
                    radial-gradient(circle at top left, rgba(31,122,92,0.12), transparent 24%),
                    radial-gradient(circle at top right, rgba(163, 212, 192, 0.30), transparent 22%),
                    linear-gradient(180deg, #fdfefd 0%, #f5f8f5 42%, #edf3ef 100%);
                color: #16211c;
            }}
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #f8fbf8 0%, #eef4ef 100%);
                border-right: 1px solid rgba(31,122,92,0.10);
            }}
            [data-testid="stSidebar"] * {{
                color: #16211c;
            }}
            .block-container {{
                padding-top: 2rem;
                padding-bottom: 2.5rem;
            }}
            div[data-testid="stMetric"] {{
                background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(244,247,243,0.98));
                border: 1px solid rgba(31,122,92,0.10);
                padding: 1rem 1.1rem;
                border-radius: 18px;
                box-shadow: 0 16px 34px rgba(17, 37, 28, 0.08);
            }}
            div[data-testid="stMetricLabel"] {{
                color: {TEXT_MUTED};
            }}
            div[data-testid="stMetricValue"] {{
                color: #16211c;
            }}
            .hero-card {{
                background: linear-gradient(135deg, rgba(255,255,255,0.98), rgba(243,248,244,0.98));
                border: 1px solid rgba(31,122,92,0.12);
                border-radius: 24px;
                padding: 1.6rem 1.6rem 1.5rem 1.6rem;
                box-shadow: 0 22px 64px rgba(17, 37, 28, 0.08);
            }}
            .hero-kicker {{
                color: {ACCENT};
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.18rem;
                font-weight: 700;
            }}
            .hero-title {{
                font-size: 2.5rem;
                line-height: 1.02;
                margin: 0.55rem 0 0.75rem 0;
                font-weight: 800;
            }}
            .hero-copy {{
                color: #3d4b44;
                font-size: 1rem;
                max-width: 58rem;
                margin-bottom: 0;
            }}
            .mini-pill-row {{
                display: flex;
                gap: 0.65rem;
                flex-wrap: wrap;
                margin-top: 1rem;
            }}
            .mini-pill {{
                border: 1px solid rgba(31,122,92,0.14);
                background: rgba(31,122,92,0.06);
                color: #1f4e3e;
                padding: 0.45rem 0.75rem;
                border-radius: 999px;
                font-size: 0.85rem;
            }}
            .section-label {{
                color: {ACCENT};
                text-transform: uppercase;
                letter-spacing: 0.18rem;
                font-size: 0.74rem;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }}
            .panel-title {{
                font-size: 1.3rem;
                margin: 0 0 0.25rem 0;
                font-weight: 750;
            }}
            .panel-copy {{
                color: {TEXT_MUTED};
                margin-bottom: 1rem;
            }}
            .profile-card {{
                background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(243,248,244,0.98));
                border: 1px solid rgba(31,122,92,0.12);
                border-radius: 22px;
                padding: 1.2rem;
                height: 100%;
            }}
            .profile-name {{
                font-size: 1.6rem;
                margin-bottom: 0.2rem;
                font-weight: 800;
            }}
            .profile-sub {{
                color: {TEXT_MUTED};
                margin-bottom: 1rem;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.8rem;
            }}
            .info-item {{
                background: rgba(31,122,92,0.04);
                border: 1px solid rgba(31,122,92,0.08);
                border-radius: 14px;
                padding: 0.7rem 0.8rem;
            }}
            .info-label {{
                color: {TEXT_MUTED};
                font-size: 0.8rem;
                margin-bottom: 0.15rem;
            }}
            .info-value {{
                font-size: 1.02rem;
                font-weight: 700;
                color: #16211c;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def build_scatter(df_filtered: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    palette = {"Pepite detectee": ACCENT, "Profil standard": "#82b39f"}

    for label, frame in df_filtered.groupby("is_gem"):
        fig.add_trace(
            go.Scatter(
                x=frame["market_value_m"],
                y=frame["potential"],
                mode="markers",
                name=label,
                text=frame["long_name"],
                customdata=np.stack(
                    [frame["club_name"], frame["overall"], frame["age"]], axis=-1
                ),
                marker=dict(
                    size=np.clip(frame["overall"].fillna(60) - 40, 10, 28),
                    color=palette.get(label, "#89a398"),
                    opacity=0.82,
                    line=dict(color="rgba(255,255,255,0.85)", width=1),
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Club: %{customdata[0]}<br>"
                    "Valeur: %{x:.1f} M EUR<br>"
                    "Potential: %{y}<br>"
                    "Overall: %{customdata[1]}<br>"
                    "Age: %{customdata[2]}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="Carte du marche: potentiel vs valeur",
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=56, b=10),
        legend=dict(orientation="h", y=1.08, x=0.01),
        xaxis=dict(
            title="Market value (M EUR)",
            gridcolor=LINE,
            zeroline=False,
        ),
        yaxis=dict(
            title="Potential",
            gridcolor=LINE,
            zeroline=False,
        ),
    )
    return fig


def build_bar_chart(df_filtered: pd.DataFrame) -> go.Figure:
    shortlist = (
        df_filtered.dropna(subset=["value_index"])
        .sort_values(["value_index", "potential"], ascending=[False, False])
        .head(10)
        .sort_values("value_index", ascending=True)
    )

    fig = go.Figure(
        go.Bar(
            x=shortlist["value_index"],
            y=shortlist["long_name"],
            orientation="h",
            marker=dict(
                color=shortlist["potential"],
                colorscale=[
                    [0.0, "#bfd8cc"],
                    [0.5, "#73ad95"],
                    [1.0, ACCENT],
                ],
                line=dict(color="rgba(255,255,255,0.08)", width=1),
                colorbar=dict(title="Potential"),
            ),
            customdata=np.stack(
                [shortlist["market_value_m"], shortlist["overall"], shortlist["age"]],
                axis=-1,
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Value index: %{x:.2f}<br>"
                "Valeur: %{customdata[0]:.1f} M EUR<br>"
                "Overall: %{customdata[1]}<br>"
                "Age: %{customdata[2]}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title="Top 10 des profils les plus rentables",
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=56, b=10),
        xaxis=dict(title="Indice rendement / prix", gridcolor=LINE),
        yaxis=dict(title="", gridcolor="rgba(0,0,0,0)"),
    )
    return fig


def build_radar(player: pd.Series) -> go.Figure:
    categories = ["Pace", "Shooting", "Passing", "Dribbling", "Physic"]
    player_values = [
        player.get("pace", np.nan),
        player.get("shooting", np.nan),
        player.get("passing", np.nan),
        player.get("dribbling", np.nan),
        player.get("physic", np.nan),
    ]

    benchmark_values = [
        float(df_filtered["pace"].median()),
        float(df_filtered["shooting"].median()),
        float(df_filtered["passing"].median()),
        float(df_filtered["dribbling"].median()),
        float(df_filtered["physic"].median()),
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=benchmark_values,
            theta=categories,
            fill="toself",
            name="Median shortlist",
            line_color="#8bb7a3",
            fillcolor="rgba(139, 183, 163, 0.22)",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=player_values,
            theta=categories,
            fill="toself",
            name=player["long_name"],
            line_color=ACCENT,
            fillcolor="rgba(31, 122, 92, 0.24)",
        )
    )

    fig.update_layout(
        title="Empreinte technique du joueur",
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=56, b=20),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=LINE),
            angularaxis=dict(gridcolor=LINE),
            bgcolor="rgba(0,0,0,0)",
        ),
        legend=dict(orientation="h", y=1.10, x=0.0),
    )
    return fig


inject_css()

try:
    df = load_data()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.stop()


st.sidebar.markdown("## Scout Console")
st.sidebar.caption("Filtrage des cibles offensives selon budget, age et niveau minimum.")

budget_min, budget_max = st.sidebar.slider(
    "Fourchette budget (EUR)",
    min_value=0,
    max_value=int(df["market_value_in_eur"].max()),
    value=(0, min(12_000_000, int(df["market_value_in_eur"].max()))),
    step=500_000,
)

age_max = st.sidebar.slider(
    "Age maximum",
    min_value=int(df["age"].min()),
    max_value=int(df["age"].max()),
    value=23,
)

overall_min = st.sidebar.slider(
    "Overall minimum",
    min_value=int(df["overall"].min()),
    max_value=int(df["overall"].max()),
    value=70,
)

positions = sorted(
    {
        pos.strip()
        for value in df["player_positions"].dropna()
        for pos in str(value).split(",")
    }
)
default_positions = [pos for pos in ["ST", "CF", "LW", "RW"] if pos in positions]
selected_positions = st.sidebar.multiselect(
    "Postes offensifs",
    options=positions,
    default=default_positions,
)

show_only_gems = st.sidebar.toggle("Afficher seulement les pepites", value=False)

df_filtered = df[
    (df["market_value_in_eur"] >= budget_min)
    & (df["market_value_in_eur"] <= budget_max)
    & (df["age"] <= age_max)
    & (df["overall"] >= overall_min)
].copy()

if selected_positions:
    pattern = "|".join(selected_positions)
    df_filtered = df_filtered[
        df_filtered["player_positions"].fillna("").str.contains(pattern, regex=True)
    ]

if show_only_gems:
    df_filtered = df_filtered[df_filtered["is_gem"] == "Pepite detectee"]

df_filtered = df_filtered.sort_values(
    ["value_index", "potential", "overall"], ascending=[False, False, False]
)

gem_count = int((df_filtered["is_gem"] == "Pepite detectee").sum())
avg_price = float(df_filtered["market_value_in_eur"].mean()) if not df_filtered.empty else 0.0
avg_potential = float(df_filtered["potential"].mean()) if not df_filtered.empty else 0.0
best_gap = int(df_filtered["gap_to_potential"].max()) if not df_filtered.empty else 0

st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-kicker">Transfer Window Intelligence</div>
        <div class="hero-title">Dashboard de recrutement offensive</div>
        <p class="hero-copy">
            Une vue unique pour reperer les attaquants a fort potentiel, mesurer leur
            prix de marche et comparer rapidement les profils les plus compatibles avec
            un recrutement sous contrainte.
        </p>
        <div class="mini-pill-row">
            <div class="mini-pill">{len(df)} joueurs charges</div>
            <div class="mini-pill">Focus: ligne d'attaque</div>
            <div class="mini-pill">Mode: shortlist data-driven</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
metric_cols = st.columns(4)
metric_cols[0].metric("Profils filtres", f"{len(df_filtered)}")
metric_cols[1].metric("Pepites detectees", f"{gem_count}")
metric_cols[2].metric("Prix moyen", format_currency(avg_price))
metric_cols[3].metric("Marge de progression max", f"+{best_gap}")

market_col, board_col = st.columns([1.25, 1.0], gap="large")

with market_col:
    st.markdown('<div class="section-label">Market Read</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Lecture immediate du marche</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-copy">Les bulles les plus hautes et les moins cheres sont les profils les plus attractifs.</div>',
        unsafe_allow_html=True,
    )
    if df_filtered.empty:
        st.warning("Aucun joueur ne correspond aux filtres actuels.")
    else:
        st.plotly_chart(build_scatter(df_filtered), use_container_width=True)

with board_col:
    st.markdown('<div class="section-label">Board</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Shortlist prioritaire</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="panel-copy">Potential moyen de la selection: {avg_potential:.1f}.</div>',
        unsafe_allow_html=True,
    )
    if df_filtered.empty:
        st.info("Elargis le budget ou baisse les seuils pour construire une shortlist.")
    else:
        st.plotly_chart(build_bar_chart(df_filtered), use_container_width=True)

st.markdown("")
st.markdown('<div class="section-label">Targets</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Tableau des recrues potentielles</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="panel-copy">Trie naturel par rendement / prix puis par potentiel.</div>',
    unsafe_allow_html=True,
)

table_columns = [
    "long_name",
    "club_name",
    "player_positions",
    "age",
    "overall",
    "potential",
    "market_value_in_eur",
    "gap_to_potential",
    "is_gem",
]

if df_filtered.empty:
    st.warning("La table est vide avec les filtres actuels.")
else:
    st.dataframe(
        df_filtered[table_columns],
        use_container_width=True,
        hide_index=True,
        column_config={
            "long_name": "Joueur",
            "club_name": "Club",
            "player_positions": "Postes",
            "age": st.column_config.NumberColumn("Age", format="%d"),
            "overall": st.column_config.NumberColumn("Overall", format="%d"),
            "potential": st.column_config.NumberColumn("Potential", format="%d"),
            "market_value_in_eur": st.column_config.NumberColumn(
                "Valeur",
                format="%.0f EUR",
            ),
            "gap_to_potential": st.column_config.NumberColumn("Delta potentiel", format="%d"),
            "is_gem": "Signal IA",
        },
    )

st.markdown("")
st.markdown('<div class="section-label">Player Dossier</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Analyse individuelle</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="panel-copy">Fiche rapide du joueur selectionne avec empreinte technique et contexte marche.</div>',
    unsafe_allow_html=True,
)

if not df_filtered.empty:
    selected_player = st.selectbox(
        "Choisir un joueur",
        options=df_filtered["long_name"].tolist(),
        index=0,
    )
    player = df_filtered[df_filtered["long_name"] == selected_player].iloc[0]

    dossier_col, radar_col = st.columns([0.95, 1.25], gap="large")

    with dossier_col:
        face_html = ""
        if pd.notna(player.get("player_face_url")):
            face_html = (
                f'<img src="{escape(str(player["player_face_url"]))}" '
                'style="width:150px;height:150px;object-fit:cover;'
                'border-radius:18px;margin-bottom:1rem;border:1px solid rgba(216,255,114,0.12);" />'
            )
        st.markdown(
            f"""
            <div class="profile-card">
            {face_html}
            <div class="profile-name">{escape(str(player["long_name"]))}</div>
            <div class="profile-sub">{escape(str(player.get("club_name", "Club inconnu")))} | {escape(str(player.get("player_positions", "N/A")))}</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Valeur marche</div>
                    <div class="info-value">{escape(format_currency(player["market_value_in_eur"]))}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Signal IA</div>
                    <div class="info-value">{escape(str(player["is_gem"]))}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Age</div>
                    <div class="info-value">{int(player["age"])} ans</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Pied fort</div>
                    <div class="info-value">{escape(str(player.get("preferred_foot", "N/A")))}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Overall / Potential</div>
                    <div class="info-value">{int(player["overall"])} / {int(player["potential"])}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Delta potentiel</div>
                    <div class="info-value">+{int(player["gap_to_potential"])}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Pace / Shooting</div>
                    <div class="info-value">{format_score(player.get("pace"))} / {format_score(player.get("shooting"))}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Passing / Dribbling</div>
                    <div class="info-value">{format_score(player.get("passing"))} / {format_score(player.get("dribbling"))}</div>
                </div>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with radar_col:
        st.plotly_chart(build_radar(player), use_container_width=True)
else:
    st.info("Aucune fiche joueur disponible tant que la shortlist est vide.")
