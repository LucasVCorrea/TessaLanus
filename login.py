import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

from ExtraFunctions.extras import notifications_by_day
from FileGetters.file_getter import *
from Plots.get_plot import raised_by_type, notificated_by_location, daily_payments_by_type

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
    value=payments_data["fecha_acreditacion"].max().date(),
    format="DD/MM/YYYY"
)

fecha_seleccionada_hasta = colb.date_input(
    ":material/calendar_month: Hasta",
    value=payments_data["fecha_acreditacion"].max().date(),
    min_value=fecha_seleccionada_desde,
    max_value=payments_data["fecha_acreditacion"].max().date(),
    format="DD/MM/YYYY"
)
st.divider()  ### ------ ####

fecha_desde = pd.to_datetime(fecha_seleccionada_desde)
fecha_hasta = pd.to_datetime(fecha_seleccionada_hasta)

payments_filtered = payments_data.loc[
    payments_data["fecha_acreditacion"].between(fecha_desde, fecha_hasta)
]

notification_filtered = notifications_data.loc[
    notifications_data["Fecha Lote"].between(fecha_desde, fecha_hasta)
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    ":material/payment_arrow_down: **Actas pagadas** en periodo",
    value=len(payments_filtered)
)

col2.metric(":material/attach_money: **Total recaudado** en periodo",
            value=f"${payments_filtered["total"].astype(int).sum():,.2f}",
            help=f"Indica que entre el **_{fecha_seleccionada_desde.strftime('%d/%m/%Y')}_** y el "
                 f"**_{fecha_seleccionada_hasta.strftime('%d/%m/%Y')}_** se notificaron en total "
                 f"**{len(notification_filtered)} actas**"
            )

col3.metric(":material/delivery_truck_speed: **Actas notificadas** en periodo", value=len(notification_filtered),
            help=f"Indica que entre el **_{fecha_seleccionada_desde.strftime('%d/%m/%Y')}_** y el "
                 f"**_{fecha_seleccionada_hasta.strftime('%d/%m/%Y')}_** se notificaron en total "
                 f"**{len(notification_filtered)} actas**"
            )

promedio = notifications_by_day(notification_filtered)

col4.metric(
    ":material/pace: **Promedio notificado** por Fecha",
    value=0 if pd.isna(promedio) else int(promedio),
    help=f"Indica que entre el **_{fecha_seleccionada_desde.strftime('%d/%m/%Y')}_** y el "
         f"**_{fecha_seleccionada_hasta.strftime('%d/%m/%Y')}_** se notificaron en promedio "
         f"**{0 if pd.isna(promedio) else int(promedio)} actas por día.**"
)

columna_izquierda, columna_central, columna_derecha = st.columns([2, 2, 4])
with columna_izquierda:
    container = st.container(border=True)
    with container:
        st.write("**Recaudado por Tipo de Infracción**")
        st.plotly_chart(raised_by_type(payments_filtered))

with columna_central:
    container = st.container(border=True)
    with container:
        st.write("**Notificado por Localidad**")
        st.plotly_chart(notificated_by_location(notification_filtered))

with columna_derecha:
    container = st.container(border=True)
    with container:
        st.plotly_chart(daily_payments_by_type(payments_filtered))

style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                   border_color="azure",
                   border_radius_px=30)
