import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

from Displays.camera_activity import show_camera_activity
from Displays.final_review import mostrar_pagina_nivel_5
from Displays.general_overview import show_general_overview
from Displays.notifications import mostrar_pagina_lotes
from Displays.payments import show_payments
from Displays.preescriptions import mostrar_pagina_preescriptions
from Displays.trials_activity import mostrar_pagina_juzgados
from FileGetters.file_getter import *


def interaction(rol):
    st.set_page_config(page_title="LanusUNLaM", page_icon="Icons/Diseño sin título (2).png", layout="wide",
                       initial_sidebar_state='expanded')
    #
    # from displays.juzgados import mostrar_pagina_juzgados
    # from displays.lotes import mostrar_pagina_lotes
    # from displays.nivel_5_actividad import mostrar_pagina_actividad
    # from displays.payments import mostrar_pagina
    # from utils.Styles.estilos import aplicar_estilo_dashboard
    #
    # aplicar_estilo_dashboard()

    # ------------------------
    # Control de navegación
    # ------------------------
    if "pagina_actual" not in st.session_state:
        st.session_state.pagina_actual = "inicio"

    # ------------------------
    # Menú principal
    # ------------------------
    if st.session_state.pagina_actual == "inicio":
        cola, colb, colc, cold, cole = st.columns(5)

        if cola.button("Ver **Pagos y Recaudación**", use_container_width=True, type="primary",
                       icon=":material/account_balance:",
                       help="### Información\n- Actas Pagadas\n- Medios de Pago\n- Actas Acreditadas por Fecha"):
            st.session_state.pagina_actual = "pagos"
            st.rerun()

        elif colb.button("Ver **Lotes**", use_container_width=True, type="primary", icon=":material/outgoing_mail:",
                         help="### Información\n- Actas Notificadas\n- Localidades Notificadas\n- Consultas sobre lotes"):
            st.session_state.pagina_actual = "lotes"
            st.rerun()

        elif colc.button("Ver **Actividad de Juzgados**", use_container_width=True, type="primary",
                         icon=":material/balance:",
                         help="### Información\n- Fallos Judiciales\n- Reducción de valores\n"):
            st.session_state.pagina_actual = "juzgados"
            st.rerun()

        elif cold.button("Ver **Actividad de Fiscalización**", use_container_width=True, type="primary",
                         icon=":material/computer:",
                         help="### Información\n- Actividad Diaria General\n- Actividad Diaria Por Revisor\n"):
            st.session_state.pagina_actual = "actividad"
            st.rerun()
        elif cole.button("Ver **Actas A Preescribir**", use_container_width=True, type="primary",
                         icon=":material/nest_clock_farsight_analog:"):
            st.session_state.pagina_actual = "preescribir"
            st.rerun()
        else:
            show_general_overview(get_actas_pagadas_dataframe(), get_notificaciones_dataframe())
    elif st.session_state.pagina_actual == "pagos":
        if st.button("Volver a la pantalla general", type="primary", icon=":material/keyboard_return:"):
            st.session_state.pagina_actual = "inicio"
            st.rerun()
        show_payments(get_actas_pagadas_dataframe())

    elif st.session_state.pagina_actual == "lotes":
        if st.button("Volver a la pantalla general", type="primary", icon=":material/keyboard_return:"):
            st.session_state.pagina_actual = "inicio"
            st.rerun()
        mostrar_pagina_lotes(get_notificaciones_dataframe(), get_actas_pagadas_dataframe())

    elif st.session_state.pagina_actual == "juzgados":
        if st.button("Volver a la pantalla general", type="primary", icon=":material/keyboard_return:"):
            st.session_state.pagina_actual = "inicio"
            st.rerun()
        mostrar_pagina_juzgados(get_fallos_dataframe())

    elif st.session_state.pagina_actual == "preescribir":
        if st.button("Volver a la pantalla general", type="primary", icon=":material/keyboard_return:"):
            st.session_state.pagina_actual = "inicio"
            st.rerun()
        mostrar_pagina_preescriptions(get_actas_a_preescribir())

    #
    # elif st.session_state.pagina_actual == "juzgados":
    #     if st.button("Volver a la pantalla general", type="primary", icon=":material/keyboard_return:"):
    #         st.session_state.pagina_actual = "inicio"
    #         st.rerun()
    #     mostrar_pagina_juzgados()
    #
    elif st.session_state.pagina_actual == "actividad":
        if st.button("Volver a la pantalla general", type="primary", icon=":material/keyboard_return:"):
            st.session_state.pagina_actual = "inicio"
            st.rerun()
        mostrar_pagina_nivel_5(get_actividad_nivel_5())
