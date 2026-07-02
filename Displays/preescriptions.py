import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

from Styles.estilos import aplicar_estilo_dashboard


def mostrar_pagina_preescriptions(dataframe):
    aplicar_estilo_dashboard()
    metric_a, metric_b, metric_c, metric_d, metric_e = st.columns(5)
    estado_elegido = metric_c.selectbox("Elija el Estado",
                                        options=["Todos los Estados"] + dataframe["estado"].unique().tolist(), index=0)
    metric_a, metric_b, metric_c, = st.columns(3)
    metric_a.metric("Total de Actas a Preescribir",
                    value=dataframe.loc[dataframe["estado"] == estado_elegido][
                        "acta_numero"].nunique() if estado_elegido != "Todos los Estados" else dataframe[
                        "acta_numero"].nunique())
    # metric_b.metric("Actas a Notificar Bajo Puerta",
    #                 value=dataframe.loc[dataframe["estado"] == "Acta a notificar bajo puerta"]["acta_numero"].nunique())
    # metric_c.metric("Actas a Notificar por Email",
    #                 value=dataframe.loc[dataframe["estado"] == "A notificar por email"]["acta_numero"].nunique())
    metric_b.metric("Cantidad de UFs",
                    value=f"{dataframe.loc[dataframe["estado"] == estado_elegido]["ufs"].astype(
                        int).sum() if estado_elegido != "Todos los Estados" else dataframe["ufs"].astype(int).sum():,.0f}".replace(
                        ",", "."))
    metric_c.metric("Monto Total",
                    value=f"${dataframe.loc[dataframe["estado"] == estado_elegido]["monto"].astype(int).sum() if estado_elegido != "Todos los Estados" else dataframe["monto"].astype(int).sum():,.0f}".replace(
                        ",", "."))
    # cola, colb = st.columns([2, 1])
    # with cola:
    container = st.container(border=True)
    if estado_elegido == "Todos los Estados":
        container.subheader("Total por estado", anchor=False)
        agrupado_por_estado = dataframe.groupby("estado").agg({"acta_numero": ["nunique"]}).reset_index()
        agrupado_por_estado.columns = ["Estado", "Cantidad de Actas"]
        container.dataframe(agrupado_por_estado.sort_values(by="Cantidad de Actas", ascending=False),
                            hide_index=True, width="stretch")
    else:
        container.subheader(f"Listado de Actas: _{estado_elegido}_", anchor=False)
        container.dataframe(dataframe.loc[dataframe[
                                              "estado"] == estado_elegido] if estado_elegido != "Todos los Estados" else dataframe,
                            hide_index=True, width="stretch")

    style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                       border_color="azure",
                       border_radius_px=30)
