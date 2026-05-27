import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import format
import interaction
from Styles.estilos import aplicar_estilo_login

st.set_page_config(page_title="BerissoUNLaM", layout="wide")

def mostrar_vista_admin(rol):
    interaction.interaction(rol)

with open('logs/config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'dashboard'  # Default al ingresar
if st.session_state['authentication_status'] is None:
    aplicar_estilo_login()
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        # col1m2.image('Icons/letter-b (1).png', width=100)
        login_result = authenticator.login(location='sidebar', key='Inicie sesión',
                                           fields={'Form name': ' ',
                                                   'Username': ':material/contacts_product: **Usuario**',
                                                   'Password': '**:material/key_vertical: Contraseña**',
                                                   'Login': ':material/login: :red[**Ingresar al Panel**]'})
    # st.sidebar.image("Icons/Algo Algo Algo (2).png", width=300)

    if login_result:
        name, authentication_status, username = login_result
        st.session_state['authentication_status'] = authentication_status
        st.session_state['username'] = username
        st.session_state['name'] = name
        st.rerun()
    if st.session_state['name'] != None:
        current_user = config['credentials']['usernames'][st.session_state['username']]
        role = current_user.get('role', '')
        format.registrar_historial_acceso(st.session_state['name'], st.session_state['username'], role)
if st.session_state['authentication_status']:
    # authenticator.logout(':blue[Cerrar sesión]', location='sidebar')
    current_user = config['credentials']['usernames'][st.session_state['username']]
    role = current_user.get('role', '')
    st.sidebar.success(f"Usuario: **{st.session_state['name']}**", icon=":material/person:")

    if st.sidebar.button('Ir al Panel', icon=":material/bar_chart_4_bars:", type="primary"):
        st.session_state['pagina'] = 'dashboard'
    if st.sidebar.button('Cambiar contraseña', icon=":material/key_vertical:", type="primary"):
        st.session_state['pagina'] = 'cambiar_contrasena'

    nombre_usuario = current_user.get('name', '')
    if st.session_state['pagina'] == 'dashboard':
        mostrar_vista_admin(role)

    # st.sidebar.image("Icons/Algo Algo Algo (2).png", width=300)
if st.session_state['authentication_status'] is False:
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.error('Usuario o contraseña incorrectos.', icon=":material/warning:")
