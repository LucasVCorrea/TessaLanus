from streamlit_extras.metric_cards import style_metric_cards

from Plots.get_plot import grilla_revisores_nivel_5, barplot_diario_por_revisor, show_camera_activity
from Styles.estilos import aplicar_estilo_dashboard
import streamlit as st
import pandas as pd


def mostrar_pagina_nivel_5(actividad_dataframe):
    aplicar_estilo_dashboard()
    fecha_minima = actividad_dataframe.Fecha.min()
    fecha_maxima = actividad_dataframe.Fecha.max()

    cola, colb, colc, cold, cole, colf = st.columns(6)

    with colc:
        fecha_desde = st.date_input(":material/calendar_month: **Desde**", format="DD/MM/YYYY",
                                    help=f"- Los Datos están disponibles desde **{fecha_minima.strftime('%d/%m/%Y')}** Al **{fecha_maxima.strftime('%d/%m/%Y')}**",
                                    value=fecha_maxima - pd.Timedelta(days=4))
    with cold:
        fecha_hasta = st.date_input(":material/calendar_month: **Hasta**", format="DD/MM/YYYY",
                                    min_value=fecha_desde)
    fecha_desde = pd.to_datetime(fecha_desde)
    fecha_hasta = pd.to_datetime(fecha_hasta)
    cola, colb, colc = st.columns(3)

    cola.metric("Total de **Presunciones Revisadas** **en el periodo seleccionado**",
                value=actividad_dataframe.loc[
                    (actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)][
                    "Total"].sum(),
                help=f"Entre el **{fecha_desde.strftime('%d/%m/%Y')}** y el **{fecha_hasta.strftime('%d/%m/%Y')}** se **Revisaron** {actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)][
                    "Total"].sum()} presunciones en Nivel 5")
    colb.metric("Total de **Presunciones Aceptadas** **en el periodo seleccionado**",
                value=f"{actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]["Aceptadas"].sum()} ({round((actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]["Aceptadas"].sum() / actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]["Total"].sum()) * 100, 2)}%)"
                ,
                help=f"Entre el **{fecha_desde.strftime('%d/%m/%Y')}** y el **{fecha_hasta.strftime('%d/%m/%Y')}** se **Aceptaron** {actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)][
                    "Aceptadas"].sum()} presunciones en Nivel 5")
    colc.metric("Total de **Presunciones Rechazadas** **en el periodo seleccionado**",
                value=f"{actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]["Rechazadas"].sum()} ({round((actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]["Rechazadas"].sum() / actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]["Total"].sum()) * 100, 2)}%)"
                ,
                help=f"Entre el **{fecha_desde.strftime('%d/%m/%Y')}** y el **{fecha_hasta.strftime('%d/%m/%Y')}** se **Rechazaron** {actividad_dataframe.loc[(actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)][
                    "Rechazadas"].sum()} presunciones en Nivel 5")

    actividad_diaria, actividad_por_fiscalizador, actividad_por_camara = st.tabs(
        ["Actividad Diaria", "Actividad por Revisor", "Actividad por Cámara"])
    with actividad_diaria:
        cola, colb = st.columns([2, 1])

        with cola:
            container = st.container(border=True)
        container.subheader("Actividad diaria de Nivel 5", anchor=False)
        container.caption(
            f"Desde el **{fecha_desde.strftime('%d/%m/%Y')}** hasta el **{fecha_hasta.strftime('%d/%m/%Y')}**")
        container.plotly_chart(
            barplot_diario_por_revisor(
                actividad_dataframe.loc[
                    (actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]))

        with colb:
            container = st.container(border=True)
        container.subheader("Resumen por Fecha y Revisor", anchor=False)
        container.caption(
            f"Desde el **{fecha_desde.strftime('%d/%m/%Y')}** hasta el **{fecha_hasta.strftime('%d/%m/%Y')}**")
        resumen = actividad_dataframe.loc[
            (actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]
        resumen = resumen.groupby(["Fecha", "Auditor"]).agg({"Aceptadas": ["sum"], "Rechazadas": ["sum"]}).reset_index()
        resumen.columns = ["Fecha", "Revisor", "Aceptadas", "Rechazadas"]
        resumen["Total"] = resumen["Aceptadas"] + resumen["Rechazadas"]
        resumen["Fecha"] = resumen["Fecha"].dt.date.map(lambda x: x.strftime("%d/%m/%Y"))
        container.dataframe(resumen, hide_index=True)

    with actividad_por_fiscalizador:
        container = st.container(border=True)
        container.plotly_chart(grilla_revisores_nivel_5(
            actividad_dataframe.loc[
                (actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)],
            fecha_desde.strftime('%d/%m/%Y'), fecha_hasta.strftime('%d/%m/%Y')))
    with actividad_por_camara:
        # TODO: UNCOMMENT THIS FOR THE NEXT VERSION ONLY **IF THE PROPER PEOPLE ACTUALLY CARE**
        #     info_camaras = format.get_info_actas_total()
        #     cameras = info_camaras.groupby("ubicacion").agg({"Cantidad cometidas": "sum"}).reset_index()
        #     cameras.columns = ["ubicacion", "Cantidad cometidas"]
        #     cola, colb = st.columns([3, 2])
        #     with cola:
        #         container = st.container(border=True)
        #         container.subheader("Cantidad de Infracciones cometidas por Cámara", anchor=False)
        #         container.plotly_chart(draw_mapa_siniestros(cameras))
        #
        #     info_camaras = info_camaras.loc[info_camaras["Año"] == 2026].loc[info_camaras["Mes"] == "Enero"]
        #
        #     cola, colb = st.columns([2, 3])
        #     with cola:
        #         container = st.container(border=True)
        #         container.subheader(f"Generado por Cámara en [_mes_]", anchor=False)
        #         separar_por_infraccion = container.toggle("Separar por tipo de infracción")
        #
        #         if separar_por_infraccion:
        #             container.plotly_chart(recaudado_por_camara(info_camaras, True), use_container_width=True)
        #
        #         else:
        #             info_camaras = info_camaras.groupby("ubicacion").agg({"Generado": "sum"}).reset_index()
        #
        #             container.plotly_chart(recaudado_por_camara(info_camaras, False), use_container_width=True)
        #     with colb:
        container = st.container(border=True)
        container.subheader(
            f"Actividad de Cámaras entre el {fecha_desde.strftime('%d/%m/%Y')} y el {fecha_hasta.strftime('%d/%m/%Y')}",
            anchor=False,
            help=f"- Detalla la cantidad de presunciones que se aceptaron por el municipio en cada cámara entre el **{fecha_desde.strftime('%d/%m/%Y')}** y el **{fecha_hasta.strftime('%d/%m/%Y')}**")

        nivel_5_reducido = actividad_dataframe.loc[
            (actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]
        actividad_por_camara = nivel_5_reducido.groupby("Código de cámara").agg(
            {"Aceptadas": "sum", "Rechazadas": "sum", "Total": "sum"}).reset_index()
        actividad_por_camara["% Aceptadas"] = (
                round(actividad_por_camara["Aceptadas"] / actividad_por_camara["Total"] * 100, 1)
                .astype(str) + "%"
        )

        actividad_por_camara["% Rechazadas"] = (
                round(actividad_por_camara["Rechazadas"] / actividad_por_camara["Total"] * 100, 1)
                .astype(str) + "%"
        )

        actividad_por_camara["% del total"] = (
                round(actividad_por_camara["Total"] / actividad_por_camara["Total"].sum() * 100, 1)
                .astype(str) + "%"
        )
        # eligio_ver_grafico = container.toggle("Ver gráfico")
        # if eligio_ver_grafico:
        #     container.plotly_chart(show_camera_activity(
        #         actividad_dataframe.loc[
        #             (actividad_dataframe["Fecha"] >= fecha_desde) & (actividad_dataframe["Fecha"] <= fecha_hasta)]),
        #         width="stretch")
        # else:
        container.dataframe(actividad_por_camara.sort_values(by="Total", ascending=False), hide_index=True)

    style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                       border_color="azure",
                       border_radius_px=30)
