import pandas as pd
import streamlit as st

from ExtraFunctions.extras import notifications_by_day
from Plots.get_plot import raised_by_type, notificated_by_location, daily_payments_by_type


def show_general_overview(payments_filtered, notification_filtered):
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        ":material/payment_arrow_down: **Actas pagadas** en periodo",
        value=len(payments_filtered)
    )

    col2.metric(":material/attach_money: **Total recaudado** en periodo",
                value=f"${payments_filtered["total"].astype(int).sum():,.0f}".replace(",", "."),
                help=f"Indica que entre el **_{payments_filtered["fecha_acreditacion"].min().strftime('%d/%m/%Y')}_** y el "
                     f"**_{payments_filtered["fecha_acreditacion"].max().strftime('%d/%m/%Y')}_** se notificaron en total "
                     f"**{len(notification_filtered)} actas**"
                )

    col3.metric(":material/delivery_truck_speed: **Actas notificadas** en periodo", value=len(notification_filtered),
                help=f"Indica que entre el **_{payments_filtered["fecha_acreditacion"].min().strftime('%d/%m/%Y')}_** y el "
                     f"**_{payments_filtered["fecha_acreditacion"].max().strftime('%d/%m/%Y')}_** se notificaron en total "
                     f"**{len(notification_filtered)} actas**"
                )

    promedio = notifications_by_day(notification_filtered)

    col4.metric(
        ":material/pace: **Promedio notificado** por Fecha",
        value=0 if pd.isna(promedio) else int(promedio),
        help=f"Indica que entre el **_{payments_filtered["fecha_acreditacion"].min().strftime('%d/%m/%Y')}_** y el "
             f"**_{payments_filtered["fecha_acreditacion"].max().strftime('%d/%m/%Y')}_** se notificaron en promedio "
             f"**{0 if pd.isna(promedio) else int(promedio)} actas por día.**"
    )
    col5.metric("Tasa adminstrativa",
                f"{payments_filtered["total"].astype(int).sum() - payments_filtered["total"].astype(int).sum() * 0.93:,.0f}".replace(",", "."))
    col6.metric("Valor UF", 2215)

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
            st.write("**Recaudado por día y tipo de infracción**")
            st.plotly_chart(daily_payments_by_type(payments_filtered))
