import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards

from Plots.get_plot import activity_by_judge, daily_activity_judge
from Styles.estilos import aplicar_estilo_dashboard


def mostrar_pagina_juzgados(dataframe):
    aplicar_estilo_dashboard()

    dataframe["fecha_fallo"] = pd.to_datetime(dataframe["fecha_fallo"], errors="coerce").dt.date

    cola, colb, colc, cold, cole, colf = st.columns(6)

    fecha_minima = dataframe["fecha_fallo"].min()
    fecha_maxima = dataframe["fecha_fallo"].max()

    with colf:
        container = st.container(border=True)
        vista_elegida = container.selectbox(
            "**:material/visibility: Opciones**",
            options=["Vista Particular", "Vista Detallada"]
        )

    with colc:
        fecha_desde = st.date_input(
            ":material/calendar_month: **Desde**",
            format="DD/MM/YYYY",
            help=f"- Los Datos están disponibles desde **{fecha_minima.strftime('%d/%m/%Y')}** Al **{fecha_maxima.strftime('%d/%m/%Y')}**",
            value=fecha_maxima - pd.Timedelta(days=4),
        )

    with cold:
        fecha_hasta = st.date_input(
            ":material/calendar_month: **Hasta**",
            format="DD/MM/YYYY",
            min_value=fecha_desde,
            value=fecha_maxima,
        )

    df_filtrado = dataframe.loc[
        (dataframe["fecha_fallo"] >= fecha_desde) &
        (dataframe["fecha_fallo"] <= fecha_hasta)
        ]
    dataframe_actas_canceladas = df_filtrado.loc[
        df_filtrado["estado"] == "Cancelada"
        ].copy()

    dataframe_actas_canceladas["valor_inicial"] = pd.to_numeric(
        dataframe_actas_canceladas["valor_inicial"],
        errors="coerce"
    )

    dataframe_actas_canceladas["valor_actual"] = pd.to_numeric(
        dataframe_actas_canceladas["valor_actual"],
        errors="coerce"
    )

    # Conservar solo filas donde ambas columnas sean numéricas
    dataframe_actas_canceladas = dataframe_actas_canceladas.dropna(
        subset=["valor_inicial", "valor_actual"]
    )

    dataframe_actas_canceladas["diferencia"] = (
            dataframe_actas_canceladas["valor_inicial"] -
            dataframe_actas_canceladas["valor_actual"]
    )

    dataframe_actas_canceladas["reduccion_total"] = (
            dataframe_actas_canceladas["valor_actual"] == 0
    )

    dataframe_actas_canceladas["valor_inicial"] = dataframe_actas_canceladas["valor_inicial"].astype(float)
    dataframe_actas_canceladas["valor_actual"] = dataframe_actas_canceladas["valor_actual"].astype(float)
    dataframe_actas_canceladas["diferencia"] = dataframe_actas_canceladas["valor_inicial"] - dataframe_actas_canceladas[
        "valor_actual"]
    dataframe_actas_canceladas["reduccion_total"] = dataframe_actas_canceladas["valor_actual"] == 0
    dataframe_actas_canceladas["% reduccion"] = round(
        (dataframe_actas_canceladas["diferencia"] / dataframe_actas_canceladas["valor_inicial"]) * 100, 2)
    columna_1, columna_2, columna_3, columna_4 = st.columns(4)
    columna_1.metric("**Fallos emitidos en periodo**", f"{len(df_filtrado)} Fallos")
    columna_2.metric("**Actas canceladas con reducción**", f"{len(dataframe_actas_canceladas)}")
    columna_3.metric("**Promedio de Reduccion de Montos**",
                     value=f"{dataframe_actas_canceladas.loc[dataframe_actas_canceladas["% reduccion"] > 0]['% reduccion'].mean():.2f}%",
                     help=f"Indica que a las actas que se le aplica reducción, en promedio se les reduce el **{dataframe_actas_canceladas.loc[dataframe_actas_canceladas["% reduccion"] > 0]['% reduccion'].mean():.2f}%** del valor original")
    columna_4.metric("**Total reducido en el periodo**",
                     f":red[:material/trending_down:] -${dataframe_actas_canceladas.loc[dataframe_actas_canceladas["% reduccion"] > 0]['diferencia'].sum():,.0f}".replace(
                         ",", "."))

    columna_1_, columna_2_ = st.columns([2,3])
    with columna_1_:
        container = st.container(border=True)
        container.subheader("Actividad por Juzgado", anchor=False)
        container.plotly_chart(activity_by_judge(df_filtrado))

    with columna_2_:
        container = st.container(border=True)
        container.subheader("Fallos Emitidos por Día", anchor=False)
        container.plotly_chart(daily_activity_judge(df_filtrado))
    style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                       border_color="azure",
                       border_radius_px=30)
