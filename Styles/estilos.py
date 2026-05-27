import base64

import streamlit as st


def aplicar_estilo_login():
    # Convertir imagen local a base64
    with open("Icons/Diseño sin título (2).png", "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    # Cargar CSS y reemplazar el marcador por la imagen base64
    with open("Styles/estilo_login.css") as f:
        css = f.read()
        css = css.replace("URL_IMAGEN_BASE64", f"data:image/jpeg;base64,{img_base64}")

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def aplicar_estilo_dashboard():
    with open("Styles/estilo_dashboard.css") as f:
        css = f"<style>{f.read()}</style>"
    st.markdown(css, unsafe_allow_html=True)