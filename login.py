import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

from Displays.camera_activity import show_camera_activity
from Displays.general_overview import show_general_overview
from Displays.payments import show_payments
from FileGetters.file_getter import *

st.set_page_config(
    layout="wide",
    page_title="Actividad Fotomultas Lanus",
    page_icon=":material/check:"
)

payments_data = get_actas_pagadas_dataframe()
notifications_data = get_notificaciones_dataframe()
uf_data = get_valor_uf_dataframe()

cola, colb, colc, cold, cole = st.columns([1, 1, 1, 5, 1])
cole.success("**:material/person: Usuario:** Usuario")
fecha_seleccionada_desde = cola.date_input(
    ":material/calendar_month: Desde",
    value=payments_data["fecha_acreditacion"].min().date(),
    format="DD/MM/YYYY"
)

fecha_seleccionada_hasta = colb.date_input(
    ":material/calendar_month: Hasta",
    value=payments_data["fecha_acreditacion"].max().date(),
    min_value=fecha_seleccionada_desde,
    max_value=payments_data["fecha_acreditacion"].max().date(),
    format="DD/MM/YYYY"
)
tab_general, tab_pagos, tab_camaras = st.tabs(
    [":material/apps: :blue-badge[**General**]", ":material/account_balance: :blue-badge[**Pagos**]",
     ":material/speed_camera: :blue-badge[**Actividad de Cámaras**]"])

fecha_desde = pd.to_datetime(fecha_seleccionada_desde)
fecha_hasta = pd.to_datetime(fecha_seleccionada_hasta)

payments_filtered = payments_data.loc[
    payments_data["fecha_acreditacion"].between(fecha_desde, fecha_hasta)
]

notification_filtered = notifications_data.loc[
    notifications_data["Fecha Lote"].between(fecha_desde, fecha_hasta)
]

with tab_general:
    show_general_overview(payments_filtered, notification_filtered)
with tab_pagos:
    show_payments(payments_filtered)
with tab_camaras:
    show_camera_activity()
style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                   border_color="azure",
                   border_radius_px=30)
