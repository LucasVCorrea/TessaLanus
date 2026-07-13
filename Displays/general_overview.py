import pandas as pd
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

import FileGetters.file_getter
from ExtraFunctions.extras import notifications_by_day
from Plots.get_plot import raised_by_type, notificated_by_location, daily_payments_by_type
import format
from Styles.estilos import aplicar_estilo_dashboard


def show_general_overview(payments_filtered, notification_filtered):
    st.divider()
    aplicar_estilo_dashboard()
    cola, colb, colc, cold = st.columns(4)

    with colb:
        anio = st.selectbox(":material/calendar_month: **Selecciona el año**: ",
                            sorted(payments_filtered["Año"].unique().tolist()),
                            index=len(payments_filtered["Año"].unique().tolist()) - 1)
    with colc:
        orden_meses = format.get_meses_ordenados()
        meses_ordenados = sorted(
            payments_filtered.loc[payments_filtered["Año"] == anio]["Mes"].unique(),
            key=lambda x: orden_meses.index(x)
        )
        mes = st.selectbox(
            ":material/calendar_month: **Selecciona el mes**:",
            meses_ordenados,
            index=len(meses_ordenados) - 1
        )

    payments_filtered_actual_month = payments_filtered.loc[payments_filtered["Año"] == anio].query(
        "@mes == Mes")
    notification_filtered_actual_month = notification_filtered.loc[notification_filtered["Año"] == anio].query("@mes == Mes")

    # ------------------------------------Calculo de totales para las metrics ----------------------------------
    data_pagadas_mes_anterior = format.get_mes_anterior(payments_filtered, anio, mes)
    data_notificadas_mes_anterior = format.get_mes_anterior(notification_filtered, anio, mes)
    col1, col2, col3, col4, col6 = st.columns(5)

    col1.metric(
        ":material/payment_arrow_down: **Actas pagadas** en periodo",
        value=len(payments_filtered_actual_month),
        delta = f"{len(payments_filtered_actual_month) - len(data_pagadas_mes_anterior)} respecto al mes anterior",
    )
    delta = (
            payments_filtered_actual_month["total"].astype(int).sum()
            - data_pagadas_mes_anterior["total"].astype(int).sum()
    )

    if delta < 0:
        delta_text = f"-${abs(delta):,.0f}".replace(",", ".")
    else:
        delta_text = f"+${delta:,.0f}".replace(",", ".")

    col2.metric(
        ":material/attach_money: **Total recaudado** en periodo",
        value=f"${payments_filtered_actual_month['total'].astype(int).sum():,.0f}".replace(",", "."),
        delta=delta_text + " respecto al mes anterior",
    )

    col6.metric(":material/delivery_truck_speed: **Actas notificadas** en periodo", value=len(notification_filtered_actual_month),
                help=f"Indica que entre el **_{payments_filtered_actual_month["fecha_acreditacion"].min().strftime('%d/%m/%Y')}_** y el "
                     f"**_{payments_filtered_actual_month["fecha_acreditacion"].max().strftime('%d/%m/%Y')}_** se notificaron en total "
                     f"**{len(notification_filtered_actual_month)} actas**",
                delta = f"{len(notification_filtered_actual_month) - len(data_notificadas_mes_anterior)} respecto al mes anterior"
                )

    col4.metric("**Tasa adminstrativa**",
                f"${payments_filtered_actual_month["Tasa administrativa"].astype(int).sum():,.0f}".replace(",", "."))
    col3.metric("**Recaudado por Infracciones**",
                f"${payments_filtered_actual_month["Tasa infraccion"].astype(int).sum():,.0f}".replace(",", "."))

    columna_izquierda, columna_central, columna_derecha = st.columns([2, 2, 5])
    with columna_izquierda:
        container = st.container(border=True)
        with container:
            st.subheader(f"Distribución de lo recaudado en {mes} {anio}", anchor=False)
            st.plotly_chart(raised_by_type(payments_filtered_actual_month))

    with columna_central:
        container = st.container(border=True)
        with container:
            st.subheader(f"Localidades más Notificadas en {mes} {anio}", anchor=False)
            st.plotly_chart(notificated_by_location(notification_filtered_actual_month))

    with columna_derecha:
        container = st.container(border=True)
        with container:
            st.subheader(f"Cantidad de Actas Pagadas en {mes} {anio}", anchor=False)
            st.plotly_chart(daily_payments_by_type(payments_filtered_actual_month))
    style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                       border_color="azure",
                       border_radius_px=30)
