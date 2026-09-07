import streamlit as st
import pandas as pd


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="European Football Analytics",
    page_icon="⚽",
    layout="wide"
)

# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>
        .main {
            background-color: #0e1117;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .title {
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 0px;
        }

        .subtitle {
            font-size: 18px;
            color: #9ca3af;
            margin-bottom: 30px;
        }

        [data-testid="stMetric"] {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 3px 12px rgba(0,0,0,0.2);
        }

        /* Fuerza a que los textos y números dentro de las tarjetas se vean claramente */
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="title">⚽ European Football Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Dashboard interactivo de partidos de fútbol europeo'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# CARGAR DATASET
# ============================================================

URL = (
    "https://raw.githubusercontent.com/"
    "CarlosMVH589/datasets/refs/heads/main/combined_matches.csv"
)


@st.cache_data
def cargar_datos():
    df = pd.read_csv(URL)

    df["HomeGoals"] = pd.to_numeric(
        df["HomeGoals"],
        errors="coerce"
    )

    df["AwayGoals"] = pd.to_numeric(
        df["AwayGoals"],
        errors="coerce"
    )

    df["TotalGoals"] = (
        df["HomeGoals"] + df["AwayGoals"]
    )

    return df


try:
    df = cargar_datos()

except Exception as e:
    st.error("❌ No fue posible cargar el dataset.")
    st.exception(e)
    st.stop()


# ============================================================
# FILTROS
# ============================================================

st.sidebar.header("🔎 Filtros")

ligas = sorted(df["League"].dropna().unique())

liga_seleccionada = st.sidebar.selectbox(
    "Selecciona una liga:",
    ["Todas"] + ligas
)


if liga_seleccionada != "Todas":
    datos = df[df["League"] == liga_seleccionada].copy()
else:
    datos = df.copy()


# ============================================================
# MÉTRICAS PRINCIPALES
# ============================================================

total_partidos = len(datos)

total_goles = int(datos["TotalGoals"].sum())

promedio_goles = (
    datos["TotalGoals"].mean()
    if total_partidos > 0
    else 0
)

victorias_locales = (
    datos["Result"] == "H"
).sum()

empates = (
    datos["Result"] == "D"
).sum()

victorias_visitantes = (
    datos["Result"] == "A"
).sum()


# ============================================================
# TARJETAS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "⚽ Partidos",
        f"{total_partidos:,}"
    )

with col2:
    st.metric(
        "🥅 Goles",
        f"{total_goles:,}"
    )

with col3:
    st.metric(
        "📊 Promedio de goles",
        f"{promedio_goles:.2f}"
    )

with col4:
    st.metric(
        "🏠 Victorias locales",
        f"{victorias_locales:,}"
    )


st.divider()


# ============================================================
# RESULTADOS
# ============================================================

st.subheader("📊 Resultados de los partidos")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🏠 Local",
        f"{victorias_locales:,}"
    )

with col2:
    st.metric(
        "🤝 Empates",
        f"{empates:,}"
    )

with col3:
    st.metric(
        "✈️ Visitante",
        f"{victorias_visitantes:,}"
    )


# ============================================================
# GOLES POR LIGA
# ============================================================

st.divider()

st.subheader("🥅 Goles por liga")

goles_liga = (
    datos
    .groupby("League")["TotalGoals"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(goles_liga)


# ============================================================
# PARTIDOS POR LIGA
# ============================================================

st.subheader("🏆 Partidos por liga")

partidos_liga = (
    datos
    .groupby("League")
    .size()
    .sort_values(ascending=False)
)

st.bar_chart(partidos_liga)


# ============================================================
# TABLA DE PARTIDOS
# ============================================================

st.divider()

st.subheader("📋 Partidos")

cantidad = st.slider(
    "Cantidad de partidos a mostrar:",
    min_value=10,
    max_value=100,
    value=25,
    step=5
)

tabla = datos[
    [
        "League",
        "Date",
        "HomeTeam",
        "AwayTeam",
        "HomeGoals",
        "AwayGoals",
        "Result"
    ]
].head(cantidad)

st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INFORMACIÓN DEL DATASET
# ============================================================

st.divider()

st.subheader("ℹ️ Información del dataset")

col1, col2 = st.columns(2)

with col1:

    st.write("**Número de registros:**")
    st.write(f"{len(df):,}")

    st.write("**Número de columnas:**")
    st.write(f"{len(df.columns)}")


with col2:

    st.write("**Ligas disponibles:**")
    st.write(f"{df['League'].nunique()}")

    st.write("**Equipos locales diferentes:**")
    st.write(f"{df['HomeTeam'].nunique():,}")


st.caption(
    "Fuente: European Football Matches — Kaggle. "
    "Datos cargados mediante GitHub Raw."
)