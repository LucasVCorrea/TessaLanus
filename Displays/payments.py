import streamlit as st

from FileGetters.file_getter import get_ranking_medios_de_pago
from Plots.get_plot import raised_by_type, daily_payments_by_type, tablero_heatmap, show_ranking_medios_de_pago, \
    barplot_by_type, ranking_pagos_plot


def color_tipo_infraccion(val):
    colores = {
        "PDA": "background-color: #8080ff; color: black;",
        "Fotomulta": "background-color: #cc6666; color: black;",
        "Velocidad": "background-color: #ffe066; color: black;",
        "Camara movil": "background-color: #ffaa80; color: black;",
        "Otros": "background-color: #6c757d; color: white;"
    }

    return colores.get(val, "")


def show_payments(payments_data):
    payments_data_filtered = payments_data.fillna("Otros")
    columna_izquierda, columna_central, columna_derecha = st.columns([1, 3, 1])
    columna_derecha.selectbox("**Vista Elegida**:", ["Gráficos", "Vista_2", "Vista_3"])
    tipo_infracciones_elegido = columna_central.multiselect(
        "**Seleccionar tipo de infracción**",
        options=payments_data_filtered["Tipo infraccion"].unique(),
        placeholder="Tipos de infracción",
        default=payments_data_filtered["Tipo infraccion"].unique()[0]
    )
    metric_1, columna_graficos = st.columns([1, 3])
    tipos_label = ", ".join(tipo_infracciones_elegido)
    metric_1.metric(
        f"**Recaudado por Infracciones** _({tipos_label if len(tipo_infracciones_elegido) != payments_data_filtered["Tipo infraccion"].nunique() else "Todas las infracciones"}_)",
        f"${payments_data_filtered.loc[payments_data_filtered["Tipo infraccion"].isin(tipo_infracciones_elegido)]["Tasa infraccion"].astype(int).sum():,.0f}".replace(
            ",", "."), delta=f"tocheck: {0}", help="Help")
    metric_1.metric(
        f"**Recaudado por Gastos Adm.** _({tipos_label if len(tipo_infracciones_elegido) != payments_data_filtered["Tipo infraccion"].nunique() else "Todas las infracciones"}_)",
        f"${payments_data_filtered.loc[payments_data_filtered["Tipo infraccion"].isin(tipo_infracciones_elegido)]["Tasa administrativa"].astype(int).sum():,.0f}".replace(
            ",", "."), delta=f"tocheck: {0}", help="Help")
    metric_1.metric(
        f"**Actas Pagadas** _({tipos_label if len(tipo_infracciones_elegido) != payments_data_filtered["Tipo infraccion"].nunique() else "Todas las infracciones"}_)",
        f"{len(payments_data_filtered.loc[payments_data_filtered["Tipo infraccion"].isin(tipo_infracciones_elegido)])} Actas".replace(
            ",", "."), delta=f"tocheck: {0}", help="Help")
    columna_graficos.plotly_chart(barplot_by_type(
        payments_data_filtered.loc[payments_data_filtered["Tipo infraccion"].isin(tipo_infracciones_elegido)]))

    with columna_graficos:
        columna_izquierda, columna_derecha = st.columns(2)
        columna_izquierda.caption("**Recaudado por Tipo de Infracción**")
        columna_izquierda.plotly_chart(raised_by_type(payments_data_filtered), key="adas")
        columna_derecha.caption(f"**Ranking de Medios de Pago** _({tipos_label if len(tipo_infracciones_elegido) != payments_data_filtered["Tipo infraccion"].nunique() else "Todas las infracciones"}_)")
        columna_derecha.plotly_chart(ranking_pagos_plot(get_ranking_medios_de_pago(payments_data_filtered.loc[payments_data_filtered["Tipo infraccion"].isin(tipo_infracciones_elegido)])),
                                     key="aadas")
        # columna_derecha.dataframe(get_ranking_medios_de_pago())

    #
    # columna_izquierda, columna_derecha = st.columns([2, 3])
    #
    # with columna_izquierda:
    #     container = st.container(border=True)
    #
    #     with container:
    #         st.caption("Listado de actas pagadas")
    #         df = payments_data_filtered.loc[
    #             payments_data_filtered["Tipo infraccion"].isin(tipo_infracciones_elegido)].drop(
    #             columns=["fecha_acreditacion", "created_at", "estado", "Tasa administrativa", "Tasa infraccion", "tipo",
    #                      "fecha_pago",
    #                      "medio_pago", "juzgado"]).sort_values(by="comprobante_nro", ascending=False)
    #
    #         styled_df = (
    #             df.style
    #             .map(color_tipo_infraccion, subset=["Tipo infraccion"])
    #         )
    #
    #         st.dataframe(
    #             styled_df,
    #             hide_index=True,
    #             width="stretch",
    #         )
    #         pagado_por_infraccion = payments_data_filtered.loc[
    #             payments_data_filtered["Tipo infraccion"].isin(tipo_infracciones_elegido)].groupby(
    #             "Tipo infraccion").agg(
    #             {"numero": ["nunique"], "total": ["sum"]}).reset_index()
    #         pagado_por_infraccion.columns = ["Tipo infraccion", "Actas pagadas", "Total recaudado"]
    #         pagado_por_infraccion["Total recaudado"] = pagado_por_infraccion["Total recaudado"].apply(
    #             lambda x: f"${x:,.0f}".replace(",", "."))
    #         st.caption("**Resumen de lo Recaudado por Infracción**")
    #         st.dataframe(pagado_por_infraccion.sort_values(by="Actas pagadas", ascending=False).style
    #                      .map(color_tipo_infraccion, subset=["Tipo infraccion"]), hide_index=True, width="stretch")
    #
    # with columna_derecha:
    #     st.plotly_chart(tablero_heatmap(payments_data_filtered))
    #     st.caption("**Ranking medio de pagos en 2026**")
    #     st.dataframe(get_ranking_medios_de_pago().drop(columns=["total"]), hide_index=True, width="stretch", height=200)
    #     st.write(
    #         f"**:green-badge[Total recaudado en 2026]**: **${get_ranking_medios_de_pago()["total"].sum():,.0f}**".replace(
    #             ",", "."))
