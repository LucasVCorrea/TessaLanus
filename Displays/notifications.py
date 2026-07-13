import numpy as np
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from datetime import date
import pandas as pd
from ExtraFunctions.extras import payed_notifications, to_excel_reporte
from FileGetters.file_getter import get_ranking_actualizado
from Plots.get_plot import daily_notifications_plot, notifications_by_type, daily_notifications
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
        vista_elegida = st.selectbox(":material/view_kanban: **Vista**",
                                     options=["Indicadores", "Tablas", "Consultar Notificaciones",
                                              "Consultar Infractores"], index=0)
    with cola:
        fecha_desde = st.date_input(
            ":material/calendar_month: **Fecha Desde**",
            value=max(primer_dia_mes, fecha_minima),
            min_value=fecha_minima,
            max_value=ultimo_dia_disponible,
            format="DD/MM/YYYY",
            disabled=True if vista_elegida == "Consultar Infractores" else False
        )

    with colb:
        fecha_hasta = st.date_input(
            ":material/calendar_month: **Fecha Hasta**",
            value=min(hoy, ultimo_dia_disponible),
            min_value=fecha_desde,
            max_value=ultimo_dia_disponible,
            format="DD/MM/YYYY",
            disabled=True if vista_elegida == "Consultar Infractores" else False

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
    localidad_elegida = ["Todos"]

    with colc:
        if vista_elegida != "Consultar Infractores":
            localidad_elegida = st.multiselect(
                ":material/location_on: **Elija una Localidad**",
                options=["Todos"] + sorted(lotes_filtrado["localidad"].dropna().unique().tolist()),
                default=["Todos"]
            )

    if (
            vista_elegida != "Consultar Infractores"
            and "Todos" not in localidad_elegida
    ):
        lotes_filtrado = lotes_filtrado[
            lotes_filtrado["localidad"].isin(localidad_elegida)
        ]

    if vista_elegida == "Indicadores":
        metrica_1, metrica_2, metrica_3, metrica_4, metrica_6 = st.columns(5)
        metrica_1.metric(
            f"**Total de Actas notificadas** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}",
            value=f":red[:material/stacked_email:] {lotes_filtrado["acta_id"].nunique()}")
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

        # metrica_4.metric(
        #     f"**Notificaciones Sentencia** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}**",
        #     value=0)
        # # metrica_4.metric("**Recaudado por Notificacion Sentencia**", value = 0)
        #
        # metrica_4.metric(
        #     f"**Notificaciones Fehaciente Por Correo** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}**",
        #     value=0)
        # metrica_5.metric("**Recaudado por Fehaciente Por Correo**", value = 0)

        metrica_4.metric(
            f"**Total de Actas pagadas** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}",
            value=f"{payed_notifications(lotes_filtrado, payments_dataframe, how="inner")['acta_id'].nunique()} Actas")
        metrica_6.metric(
            f"**Monto de Actas pagadas** del {fecha_desde.strftime("%d/%m/%Y")} al {fecha_hasta.strftime("%d/%m/%Y")}",
            value=f":green[:material/paid:] {payed_notifications(lotes_filtrado, payments_dataframe, "inner")['total'].astype(int).sum():,.0f}".replace(
                ",", "."))

        columna_barplot, columna_donut = st.columns([2, 1])
        with columna_donut:
            container = st.container(border=True)
            container.subheader("Actas Notificadas Por Tipo", anchor=False)
            container.plotly_chart(notifications_by_type(lotes_filtrado), width="stretch")
            cola, colb = st.columns(2)
            pagadas = payed_notifications(lotes_filtrado, payments_dataframe, "inner")
            cola.metric(":red[:material/attach_email:] Email Pagadas",
                        pagadas.loc[pagadas["notific_type"] == "Email", "acta_id"].nunique())
            colb.metric(":orange[:material/garage_door:] Bajo Puerta Pagadas",
                        pagadas.loc[pagadas["notific_type"] == "Bajo Puerta", "acta_id"].nunique())

        with columna_barplot:
            container = st.container(border=True)
            container.subheader("Cantidad de Actas notificadas por Localidad", anchor=False)
            # actas_por_localidad = lotes_filtrado.groupby("localidad")["acta_id"].nunique().reset_index()
            # actas_por_localidad.columns = ["Localidad", "Cantidad de Actas Notificadas"]
            container.plotly_chart(daily_notifications(lotes_filtrado))

    elif vista_elegida == "Tablas":
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
    elif vista_elegida == "Consultar Notificaciones":
        dataframe = payed_notifications(lotes_filtrado, payments_dataframe, "left")
        actas_pagadas_de_lotes_filtrados_second = dataframe.copy()
        actas_pagadas_de_lotes_filtrados_second["Fecha Lote"] = pd.to_datetime(
            actas_pagadas_de_lotes_filtrados_second["Fecha Lote"],
            errors="coerce",
            dayfirst=True
        )
        if "pagina_lotes" not in st.session_state:
            st.session_state.pagina_lotes = 1
        tam_pagina = 8

        actas_pagadas_de_lotes_filtrados_second["fecha_acreditacion"] = pd.to_datetime(
            actas_pagadas_de_lotes_filtrados_second["fecha_acreditacion"],
            errors="coerce",
            dayfirst=True
        )
        col_filtro_1, col_filtro_2, col_filtro_3, col_filtro_4, col_filtro_5 = st.columns(5)
        actas_pagadas_de_lotes_filtrados_second["Tiempo hasta el pago"] = (
                actas_pagadas_de_lotes_filtrados_second["fecha_acreditacion"] - actas_pagadas_de_lotes_filtrados_second[
            "Fecha Lote"]
        ).dt.days
        actas_pagadas_de_lotes_filtrados_second["Estado"] = np.where(
            actas_pagadas_de_lotes_filtrados_second["fecha_acreditacion"].isna(),
            "No pagada",
            "Pagada"
        )
        with col_filtro_1:
            estado_elegido = st.selectbox(
                "Estado",
                options=["Todas"] + sorted(
                    actas_pagadas_de_lotes_filtrados_second["Estado"].dropna().unique().tolist()),
                key="filtro_estado_pagada"
            )

        with col_filtro_2:
            tipo_notificacion_elegido = st.selectbox(
                "Tipo Notificación",
                options=["Todas"] + sorted(
                    actas_pagadas_de_lotes_filtrados_second["notific_type"].dropna().unique().tolist()),
                key="filtro_tipo_notificacion"
            )
        if estado_elegido != "Todas":
            actas_pagadas_de_lotes_filtrados_second = actas_pagadas_de_lotes_filtrados_second.loc[
                actas_pagadas_de_lotes_filtrados_second["Estado"] == estado_elegido]

        if tipo_notificacion_elegido != "Todas":
            actas_pagadas_de_lotes_filtrados_second = actas_pagadas_de_lotes_filtrados_second.loc[
                actas_pagadas_de_lotes_filtrados_second["notific_type"] == tipo_notificacion_elegido]

        total_filas = len(actas_pagadas_de_lotes_filtrados_second)
        total_paginas = max(1, (total_filas - 1) // tam_pagina + 1)

        if st.session_state.pagina_lotes > total_paginas:
            st.session_state.pagina_lotes = total_paginas

        inicio = (st.session_state.pagina_lotes - 1) * tam_pagina
        fin = inicio + tam_pagina

        df_pagina = actas_pagadas_de_lotes_filtrados_second.iloc[inicio:fin]

        st.caption(f"Resultados encontrados: {total_filas}")

        container = st.container(border=True)

        with container:
            h1, h2, h3, h4, h5, h6, h7, h8, h9 = st.columns([1, 1, 3, 3, 2, 2, 2, 2, 2])

            h1.markdown("**Tipo**")
            h2.markdown("**Acta**")
            h3.markdown("**Nombre**")
            h4.markdown("**Calle**")
            h5.markdown("**Localidad**")
            h6.markdown("**Fecha Lote**")
            h7.markdown("**Estado**")
            h8.markdown("**Pago acreditado**")
            h9.markdown("**Tiempo hasta el pago**")

            if df_pagina.empty:
                st.info("No se encontraron resultados con los filtros seleccionados.")

            for _, row in df_pagina.iterrows():

                col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 3, 3, 2, 2, 2, 2, 2])

                with col1:
                    if row["notific_type"] == "Email":
                        st.badge("**Email**", color="blue")
                    elif row["notific_type"] == "Bajo Puerta":
                        st.badge("**Bajo Puerta**", color="violet")
                    else:
                        st.badge(str(row["notific_type"]))

                col2.markdown(
                    f"[{row['acta']}](https://lanus.infratrack.com.ar/actas/{row['acta']})"
                )
                col3.write(f"**{row.get("nombre_x", row.get("nombre", ""))}**")
                col4.write(f"**{row["calle"]}**")
                col5.write(f"**{row["localidad"]}**")
                col6.write(f"**{row["Fecha Lote"]}**")
                col8.write(
                    f"**{row["fecha_acreditacion"]}**" if pd.notna(row["fecha_acreditacion"]) else "**No acreditado**")
                col9.write(
                    str(f"**{row["Tiempo hasta el pago"]}**") + " **Días**" if pd.notna(
                        row["Tiempo hasta el pago"]) else "N/A")
                with col7:
                    if row["Estado"] == "Pagada":
                        st.badge("**Pagada**", color="green")
                    elif row["Estado"] == "No pagada":
                        st.badge("**No pagada**", color="red")
                    else:
                        st.badge(str(row["Estado"]))

                st.divider()

        col_pag_1, col_pag_2, col_pag_3 = st.columns([1, 2, 1])

        with col_pag_1:
            if st.button(
                    ":blue[Anterior]",
                    disabled=st.session_state.pagina_lotes <= 1,
                    icon=":material/keyboard_double_arrow_left:"
            ):
                st.session_state.pagina_lotes -= 1
                st.rerun()

        with col_pag_2:
            st.markdown(
                f"<div style='text-align:center;'>Página {st.session_state.pagina_lotes} de {total_paginas}</div>",
                unsafe_allow_html=True
            )

        with col_pag_3:
            if st.button(
                    ":blue[Siguiente]",
                    disabled=st.session_state.pagina_lotes >= total_paginas,
                    icon=":material/keyboard_double_arrow_right:"
            ):
                st.session_state.pagina_lotes += 1
                st.rerun()
    else:
        data_infractores = get_ranking_actualizado()

        with colc:
            localidad_elegida = st.multiselect(
                "Elija la localidad:",
                options=["Todas"] + sorted(data_infractores["Localidad"].dropna().unique().tolist()),
                default=["Todas"]
            )

        if "Todas" in localidad_elegida:
            data_infractores_filtrado = data_infractores
        else:
            data_infractores_filtrado = data_infractores[
                data_infractores["Localidad"].isin(localidad_elegida)
            ]
        resumen = (
            data_infractores_filtrado
            .assign(**{
                "Monto Total": pd.to_numeric(
                    data_infractores_filtrado["Monto Total"],
                    errors="coerce"
                ).fillna(0)
            })
            .groupby("Localidad", as_index=False)
            .agg(
                **{
                    "Cantidad a notificar": ("Localidad", "size"),
                    "Monto a cobrar": ("Monto Total", "sum")
                }
            )
            .sort_values("Cantidad a notificar", ascending=False)
        )

        tabla = "| Localidad | Cantidad a notificar | Monto Total a cobrar (sin pago voluntario) |\n"
        tabla += "|:----------|----------------------:|---------------:|\n"

        for _, fila in resumen.iterrows():
            tabla += (
                    f"| {fila['Localidad']} "
                    f"| {fila['Cantidad a notificar']:,}".replace(",", ".")
                    + f" | ${fila['Monto a cobrar']:,.0f}".replace(",", ".")
                    + " |\n"
            )

        # Totales
        total_registros = resumen["Cantidad a notificar"].sum()
        total_monto = resumen["Monto a cobrar"].sum()

        tabla += (
                f"| **TOTAL** "
                f"| **{total_registros:,}**".replace(",", ".")
                + f" | **${total_monto:,.0f}**".replace(",", ".")
                + " |\n"
        )

        st.markdown(tabla)
        ranking_table_excel = to_excel_reporte(
            data_infractores_filtrado)
        st.download_button(
            label=":green-badge[:material/table: **Descargar Ranking en Excel**]",
            data=ranking_table_excel,
            file_name="ranking_infractores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                       border_color="azure",
                       border_radius_px=30)
