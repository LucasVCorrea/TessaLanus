import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from datetime import date
import pandas as pd
from ExtraFunctions.extras import payed_notifications
from Plots.get_plot import daily_notifications_plot, notifications_by_type
from Styles.estilos import aplicar_estilo_dashboard


def mostrar_pagina_lotes(notifications_dataframe, payments_dataframe):
    aplicar_estilo_dashboard()

    # Asegurar formato datetime
    notifications_dataframe["Fecha Lote"] = pd.to_datetime(
        notifications_dataframe["Fecha Lote"],
        errors="coerce"
    )

    # Obtener mes actual
    hoy = date.today()

    ultimo_dia_disponible = notifications_dataframe["Fecha Lote"].max().date()

    fecha_base = min(hoy, ultimo_dia_disponible)
    primer_dia_mes = fecha_base.replace(day=1)
    fecha_minima = notifications_dataframe["Fecha Lote"].min().date()

    cola, colb, colc, cold = st.columns([1, 1, 11, 2])
    with cold:
        vista_elegida = st.selectbox(":material/view_kanban: **Vista**", options=["Indicadores", "Tablas"], index=0)
    with cola:
        fecha_desde = st.date_input(
            ":material/calendar_month: **Fecha Desde**",
            value=max(primer_dia_mes, fecha_minima),
            min_value=fecha_minima,
            max_value=ultimo_dia_disponible,
            format="DD/MM/YYYY"
        )

    with colb:
        fecha_hasta = st.date_input(
            ":material/calendar_month: **Fecha Hasta**",
            value=min(hoy, ultimo_dia_disponible),
            min_value=fecha_desde,
            max_value=ultimo_dia_disponible,
            format="DD/MM/YYYY"
        )

    lotes_filtrado = notifications_dataframe[
        (
                notifications_dataframe["Fecha Lote"].dt.date >= fecha_desde
        )
        &
        (
                notifications_dataframe["Fecha Lote"].dt.date <= fecha_hasta
        )
        ]
    with colc:
        localidad_elegida = st.multiselect(":material/location_on: **Elija una Localidad**",
                                           options=lotes_filtrado["localidad"].unique(),
                                           default="CABA")
    lotes_filtrado = lotes_filtrado[
        lotes_filtrado["localidad"].isin(localidad_elegida)] if localidad_elegida else lotes_filtrado

    metrica_1, metrica_2, metrica_3, metrica_4, metrica_5,metrica_6 = st.columns(6)
    metrica_1.metric(
        f"**Total de Actas notificadas** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}",
        value=f":red[:material/stacked_email:] {lotes_filtrado["acta_id"].nunique()}", delta=f"{100}")
    metrica_2.metric(f"**Por Email** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}",
                     value=f":red[:material/attach_email:] {lotes_filtrado.loc[lotes_filtrado['notific_type'] == 'Email', 'acta_id'].nunique()}",
                    )
    # metrica_2.metric("**Recaudado por Notificacion Email**", value = 0)
    metrica_3.metric(
        f"**Notificaciones Audiencia** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}",
        value=f":red[:material/garage_door:] {lotes_filtrado.loc[lotes_filtrado['notific_type'] == 'Bajo Puerta', 'acta_id'].nunique()}",
        )
    # metrica_3.metric("**Recaudado por Notificacion Audiencia**", value = f"${payed_notifications(lotes_filtrado, payments_dataframe)['total'].astype(int).sum():,.0f}".replace(
    #         ",", "."))

    metrica_4.metric(
        f"**Notificaciones Sentencia** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}**",
        value=0)
    # metrica_4.metric("**Recaudado por Notificacion Sentencia**", value = 0)

    metrica_5.metric(
        f"**Notificaciones Fehaciente Por Correo** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}**",
        value=0)
    # metrica_5.metric("**Recaudado por Fehaciente Por Correo**", value = 0)

    metrica_6.metric(
        f"**Total de Actas pagadas** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}",
        value=f":green[:material/paid:] {payed_notifications(lotes_filtrado, payments_dataframe)['acta_id'].nunique()} Actas",
        help=f"De los lotes en el periodo seleccionado, la cantidad de Actas que fueron Pagadas equivalen a **${payed_notifications(lotes_filtrado, payments_dataframe)['total'].astype(int).sum():,.0f} Pesos**".replace(
            ",", "."))

    if vista_elegida == "Indicadores":
        columna_barplot, columna_donut = st.columns([2, 1])
        with columna_donut:
            container = st.container(border=True)
            container.subheader("Actas Notificadas Por Tipo", anchor=False)
            container.plotly_chart(notifications_by_type(lotes_filtrado), width="stretch")
            cola, colb = st.columns(2)
            pagadas = payed_notifications(lotes_filtrado, payments_dataframe)
            cola.metric(":red[:material/attach_email:] Email Pagadas",
                        pagadas.loc[pagadas["notific_type"] == "Email", "acta_id"].nunique())
            colb.metric(":orange[:material/garage_door:] Bajo Puerta Pagadas",
                        pagadas.loc[pagadas["notific_type"] == "Bajo Puerta", "acta_id"].nunique())

        with columna_barplot:
            container = st.container(border=True)
            container.subheader("Cantidad de Actas notificadas por Localidad", anchor=False)
            actas_por_localidad = lotes_filtrado.groupby("localidad")["acta_id"].nunique().reset_index()
            actas_por_localidad.columns = ["Localidad", "Cantidad de Actas Notificadas"]
            container.dataframe(actas_por_localidad.sort_values(by="Cantidad de Actas Notificadas", ascending=False),
                                width="stretch", hide_index=True)
    else:
        columna_barplot, columna_donut = st.columns([2, 1])
        with columna_barplot:
            container = st.container(border=True)
            container.subheader("Cantidad de Actas notificadas por Localidad", anchor=False)
            actas_por_localidad = lotes_filtrado.groupby("localidad")["acta_id"].nunique().reset_index()
            actas_por_localidad.columns = ["Localidad", "Cantidad de Actas Notificadas"]
            container.dataframe(actas_por_localidad.sort_values(by="Cantidad de Actas Notificadas", ascending=False),
                                width="stretch", hide_index=True)
        with columna_donut:
            container = st.container(border=True)
            container.subheader("Listado de Actas notificadas en el período y localidad seleccionado/s", anchor=False)
            container.dataframe(lotes_filtrado[["acta_id", "localidad", "Fecha Lote", "notific_type"]], hide_index=True,
                                width="stretch")

    style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                       border_color="azure",
                       border_radius_px=30)

