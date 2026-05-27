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

    payments_filtered = payments_filtered.loc[payments_filtered["Año"] == anio].query(
        "@mes == Mes")
    notification_filtered = notification_filtered.loc[notification_filtered["Año"] == anio].query("@mes == Mes")

    # ------------------------------------Calculo de totales para las metrics ----------------------------------
    data_mes_anterior = format.get_mes_anterior(payments_filtered, anio, mes)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        ":material/payment_arrow_down: **Actas pagadas** en periodo",
        value=len(payments_filtered)
    )

    col2.metric(":material/attach_money: **Total recaudado** en periodo",
                value=f"${payments_filtered["total"].astype(int).sum():,.0f}".replace(",", "."),
                help=f"Indica que entre el **_{payments_filtered["fecha_acreditacion"].min().strftime('%d/%m/%Y')}_** y el "
                     f"**_{payments_filtered["fecha_acreditacion"].max().strftime('%d/%m/%Y')}_** se recaudaron en total "
                     f"**{payments_filtered["total"].astype(int).sum():,.0f}".replace(",",
                                                                                      ".") + "** pesos argentinos")

    col6.metric(":material/delivery_truck_speed: **Actas notificadas** en periodo", value=len(notification_filtered),
                help=f"Indica que entre el **_{payments_filtered["fecha_acreditacion"].min().strftime('%d/%m/%Y')}_** y el "
                     f"**_{payments_filtered["fecha_acreditacion"].max().strftime('%d/%m/%Y')}_** se notificaron en total "
                     f"**{len(notification_filtered)} actas**"
                )

    promedio = notifications_by_day(notification_filtered)

    col5.metric(
        ":material/pace: **Promedio notificado** por Fecha",
        value=0 if pd.isna(promedio) else int(promedio),
        help=f"Indica que entre el **_{payments_filtered["fecha_acreditacion"].min().strftime('%d/%m/%Y')}_** y el "
             f"**_{payments_filtered["fecha_acreditacion"].max().strftime('%d/%m/%Y')}_** se notificaron en promedio "
             f"**{0 if pd.isna(promedio) else int(promedio)} actas por día.**"
    )
    col4.metric("**Tasa adminstrativa**",
                f"${payments_filtered["Tasa administrativa"].astype(int).sum():,.0f}".replace(",", "."))
    col3.metric("**Recaudado por Infracciones**", f"${payments_filtered["Tasa infraccion"].astype(int).sum():,.0f}".replace(",", "."))

    columna_izquierda, columna_central, columna_derecha = st.columns([2, 2, 5])
    with columna_izquierda:
        container = st.container(border=True)
        with container:
            st.subheader(f"Distribución de lo recaudado en {mes} {anio}", anchor=False)
            st.plotly_chart(raised_by_type(payments_filtered))

    with columna_central:
        container = st.container(border=True)
        with container:
            st.subheader(f"Distribución de Localidades Notificadas en {mes} {anio}", anchor=False)
            st.plotly_chart(notificated_by_location(notification_filtered))

    with columna_derecha:
        container = st.container(border=True)
        with container:
            st.subheader(f"Cantidad de Actas Pagadas en {mes} {anio}", anchor=False)
            st.plotly_chart(daily_payments_by_type(payments_filtered))
    style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                       border_color="azure",
                       border_radius_px=30)