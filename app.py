import streamlit as st
import sys
import os
import base64
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from rag import preguntar_agente

st.set_page_config(
    page_title="FarmaKnow",
    page_icon="assets/farmaknow.png" if os.path.exists("assets/farmaknow.png") else None,
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;0,900;1,400&display=swap');

html, body, [class*="st-"], p, li {
    font-family: 'Roboto', sans-serif;
}

h1, h2, h3 {
    font-family: 'Roboto', sans-serif !important;
    font-weight: 900 !important;
}

button[kind="pills"], div[data-testid="stPills"] button,
div[data-testid="stSegmentedControl"] button {
    font-family: 'Roboto', sans-serif !important;
    border-radius: 999px !important;
    border: 1px solid #333333 !important;
}

div[data-testid="stPills"] button[aria-checked="true"],
div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-weight: 700 !important;
}

.stButton > button {
    font-family: 'Roboto', sans-serif !important;
    background-color: #FFFFFF;
    color: #000000;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.6rem 1.4rem;
    width: 100%;
}
.stButton > button:hover { background-color: #d9d9d9; color: #000000; }

/* Imagen-boton del menu */
.icono-btn {
    display: block;
    transition: transform 0.15s ease, filter 0.15s ease;
}
.icono-btn:hover {
    transform: scale(1.06);
    filter: brightness(1.15);
    cursor: pointer;
}
.icono-desc {
    text-align: center;
    color: #b5b5b5;
    font-size: 0.92rem;
    margin-top: 0.5rem;
    line-height: 1.45;
}

/* Boton home */
.home-btn {
    display: inline-block;
    transition: transform 0.15s ease, filter 0.15s ease;
}
.home-btn:hover {
    transform: scale(1.1);
    filter: brightness(1.2);
}

.respuesta-card {
    background-color: #0d0d0d;
    border: 1px solid #2a2a2a;
    border-left: 4px solid #FFFFFF;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
    line-height: 1.7;
}

.fuentes-card {
    background-color: #0d0d0d;
    border: 1px solid #262626;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-top: 0.6rem;
    font-size: 0.92rem;
    color: #b5b5b5;
}
.fuentes-card b { color: #e5e5e5; }

.farmaknow-tagline {
    text-align: center;
    color: #9a9a9a;
    font-style: italic;
    margin-top: -0.6rem;
    font-size: 1.05rem;
}

.stChatMessage {
    background-color: #0d0d0d;
    border: 1px solid #262626;
    border-radius: 12px;
}

hr { border-color: #262626; }
</style>
""", unsafe_allow_html=True)

# ---------- HELPERS DE IMAGEN ----------
def img_base64(ruta):
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode()

def imagen_boton(ruta_png, destino, descripcion):
    """Renderiza una imagen clicable que navega a ?pantalla=destino"""
    if not os.path.exists(ruta_png):
        return
    b64 = img_base64(ruta_png)
    st.markdown(
        f"""
        <a href="?pantalla={destino}" target="_self" class="icono-btn">
            <img src="data:image/png;base64,{b64}" style="width:100%;" />
        </a>
        <p class="icono-desc">{descripcion}</p>
        """,
        unsafe_allow_html=True,
    )

def boton_home():
    if os.path.exists("assets/home.png"):
        b64 = img_base64("assets/home.png")
        st.markdown(
            f"""
            <a href="?pantalla=inicio" target="_self" class="home-btn">
                <img src="data:image/png;base64,{b64}" style="width:52px;" />
            </a>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<a href="?pantalla=inicio" target="_self">Inicio</a>', unsafe_allow_html=True)

# ---------- ESTADO / ROUTER ----------
pantalla = st.query_params.get("pantalla", "inicio")

if "historial" not in st.session_state:
    st.session_state.historial = []

# ---------- DATOS ----------
NOMBRES_GRUPOS = {
    "dolor_fiebre_inflamacion": "Dolor y fiebre",
    "respiratorio_gripe": "Gripe y alergias",
    "digestivo": "Digestivo",
    "dermatologico_topico": "Piel",
    "herbolaria_vitaminas": "Herbolaria y vitaminas",
}

@st.cache_data
def cargar_sintomas():
    df = pd.read_csv("docs/catalogo_unificado.csv")
    return {
        grupo: sorted(df[df["grupo"] == grupo]["sintoma"].unique())
        for grupo in df["grupo"].unique()
    }

sintomas_por_grupo = cargar_sintomas()

# ---------- HELPERS DE RESPUESTA ----------
def html_fuentes(metadatas):
    items = []
    for m in metadatas:
        if m.get("tipo") == "medicamento":
            nombre = m.get("nombre_comercial", "N/A")
            grupo = NOMBRES_GRUPOS.get(m.get("grupo", ""), m.get("grupo", ""))
            items.append(f"<b>{nombre}</b> ({grupo})")
    if not items:
        return ""
    return "<div class='fuentes-card'>Fuentes del catalogo consultadas: " + " · ".join(items) + "</div>"

def mostrar_respuesta(respuesta, hay_alerta, metadatas):
    if hay_alerta:
        st.error("Atencion: tu consulta incluye un posible sintoma de alerta. "
                 "Si es tu caso, busca atencion medica de inmediato.")
    st.markdown(f"<div class='respuesta-card'>{respuesta}</div>", unsafe_allow_html=True)
    fuentes = html_fuentes(metadatas)
    if fuentes:
        st.markdown(fuentes, unsafe_allow_html=True)

def encabezado(con_home=False):
    if con_home:
        boton_home()
    if os.path.exists("assets/farmaknow.png"):
        c1, c2, c3 = st.columns([1.2, 1, 1.2])
        with c2:
            st.image("assets/farmaknow.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center;'>FarmaKnow</h1>", unsafe_allow_html=True)
    st.markdown("<p class='farmaknow-tagline'>Orientacion sobre medicamentos de venta libre, herbolaria y suplementos en Mexico</p>", unsafe_allow_html=True)
    st.markdown("---")

# ---------- PANTALLA: INICIO ----------
def pantalla_inicio():
    encabezado()
    st.markdown("<h3 style='text-align:center;'>¿Como quieres consultar?</h3>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        imagen_boton(
            "assets/consultaguiada.png",
            "guiada",
            "Selecciona tus sintomas de una lista organizada por categorias y recibe opciones de venta libre.",
        )

    with col2:
        imagen_boton(
            "assets/chatlibre.png",
            "chat",
            "Escribe tu malestar con tus propias palabras y conversa con el asistente.",
        )

    with col3:
        imagen_boton(
            "assets/acercade.png",
            "acerca",
            "Conoce que hace FarmaKnow, sus limites, fuentes y la tecnologia detras.",
        )

# ---------- PANTALLA: CONSULTA GUIADA ----------
def pantalla_guiada():
    encabezado(con_home=True)
    st.markdown("## Consulta Guiada")

    st.markdown("#### 1. ¿En que area sientes el malestar?")
    grupo_elegido = st.segmented_control(
        "Categoria",
        options=list(NOMBRES_GRUPOS.keys()),
        format_func=lambda g: NOMBRES_GRUPOS[g],
        label_visibility="collapsed",
    )

    if grupo_elegido:
        st.markdown("#### 2. Toca los sintomas que tienes")
        sintomas_elegidos = st.pills(
            "Sintomas",
            options=sintomas_por_grupo[grupo_elegido],
            selection_mode="multi",
            label_visibility="collapsed",
        )

        if sintomas_elegidos:
            st.markdown("#### 3. Consulta")
            if st.button("Buscar opciones de venta libre"):
                consulta = ", ".join(sintomas_elegidos)
                with st.spinner("Consultando el catalogo FarmaKnow..."):
                    respuesta, hay_alerta, metadatas = preguntar_agente(consulta)
                mostrar_respuesta(respuesta, hay_alerta, metadatas)

# ---------- PANTALLA: CHAT LIBRE ----------
def pantalla_chat():
    encabezado(con_home=True)
    st.markdown("## Chat Libre")

    for autor, mensaje in st.session_state.historial:
        with st.chat_message(autor):
            st.markdown(mensaje)

    pregunta = st.chat_input("Describe tu malestar con tus propias palabras...")
    if pregunta:
        st.session_state.historial.append(("user", pregunta))
        with st.chat_message("user"):
            st.markdown(pregunta)

        with st.spinner("Consultando el catalogo FarmaKnow..."):
            respuesta, hay_alerta, metadatas = preguntar_agente(pregunta)

        with st.chat_message("assistant"):
            if hay_alerta:
                st.error("Atencion: tu consulta incluye un posible sintoma de alerta.")
            st.markdown(respuesta)

        fuentes = html_fuentes(metadatas)
        if fuentes:
            st.markdown(fuentes, unsafe_allow_html=True)

        st.session_state.historial.append(("assistant", respuesta))

# ---------- PANTALLA: ACERCA DE ----------
def pantalla_acerca():
    encabezado(con_home=True)
    st.markdown("""
## Acerca de FarmaKnow

Asistente de IA que orienta sobre **medicamentos de venta libre (OTC), herbolaria y
suplementos disponibles en Mexico**, con base en un catalogo curado de 161 registros
con fuentes como COFEPRIS, PLM, el Cuadro Basico del CSG y la Farmacopea Herbolaria.

### Lo que NO hace

- No diagnostica ni reemplaza una consulta medica
- No indica dosis: siempre remite al empaque o a un profesional
- No sugiere medicamentos que requieren receta
- Ante sintomas de alerta (dolor de pecho, sangrados, dificultad para respirar...),
  recomienda atencion medica inmediata en lugar de productos

### Tecnologia

RAG (Retrieval-Augmented Generation) con embeddings de Cohere, base vectorial ChromaDB
e interfaz Streamlit. Proyecto del programa **Oracle Next Education / Alura**.
""")

# ---------- ROUTER ----------
if pantalla == "guiada":
    pantalla_guiada()
elif pantalla == "chat":
    pantalla_chat()
elif pantalla == "acerca":
    pantalla_acerca()
else:
    pantalla_inicio()

st.markdown("---")
st.caption("FarmaKnow es un proyecto educativo. La informacion es orientativa y no sustituye la valoracion de un profesional de la salud.")
