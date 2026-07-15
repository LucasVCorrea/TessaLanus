import pandas as pd
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

    metric_b.metric("Cantidad de UFs",
                    value=f"{dataframe.loc[dataframe["estado"] == estado_elegido]["ufs"].astype(
                        int).sum() if estado_elegido != "Todos los Estados" else dataframe["ufs"].astype(int).sum():,.0f}".replace(
                        ",", "."))
    metric_c.metric("Monto Total",
                    value=f"${dataframe.loc[dataframe["estado"] == estado_elegido]["monto"].astype(int).sum() if estado_elegido != "Todos los Estados" else dataframe["monto"].astype(int).sum():,.0f}".replace(
                        ",", "."))

    container = st.container(border=True)
    if estado_elegido == "Todos los Estados":
        container.subheader("Total por estado", anchor=False)
        agrupado_por_estado = dataframe.groupby("estado").agg({"acta_numero": ["nunique"]}).reset_index()
        agrupado_por_estado.columns = ["Estado", "Cantidad de Actas"]
        container.dataframe(agrupado_por_estado.sort_values(by="Cantidad de Actas", ascending=False),
                            hide_index=True, width="stretch")
    else:
        container.subheader(f"Listado de Actas: _{estado_elegido}_", anchor=False)
        if "pagina_lotes" not in st.session_state:
            st.session_state.pagina_lotes = 1
        tam_pagina = 8

        dataframe["fecha_infraccion"] = pd.to_datetime(
            dataframe["fecha_infraccion"],
            errors="coerce",
            dayfirst=True
        ).dt.date
        dataframe["fecha_prescripcion"] = pd.to_datetime(
            dataframe["fecha_prescripcion"],
            errors="coerce",
            dayfirst=True
        ).dt.date
        dataframe["cuit"] = dataframe["cuit"].astype(str).str.replace(".0", "", regex=False).str.strip()
        dataframe["cuit"] = (
            dataframe["cuit"]
            .astype(str)
            .str.zfill(11)
            .apply(lambda x: f"{x[:2]}-{x[2:10]}-{x[10:]}")
        )
        total_filas = len(dataframe.loc[dataframe["estado"] == estado_elegido])
        total_paginas = max(1, (total_filas - 1) // tam_pagina + 1)

        if st.session_state.pagina_lotes > total_paginas:
            st.session_state.pagina_lotes = total_paginas

        inicio = (st.session_state.pagina_lotes - 1) * tam_pagina
        fin = inicio + tam_pagina

        df_pagina = dataframe.loc[dataframe["estado"] == estado_elegido].iloc[inicio:fin]

        st.caption(f"Resultados encontrados: {total_filas}")

        container = st.container(border=True)

        with container:
            h2, h3, h4, h5, h6, h7, h8, h9 = st.columns([1, 3, 3, 2, 2, 2, 2, 2])

            h2.markdown("**Acta**")
            h3.markdown("**Nombre**")
            h7.markdown("**Juzgado**")
            h5.markdown("**Cuit**")
            h6.markdown("**Fecha Infracción**")
            h4.markdown("**Estado**")
            h8.markdown("**UFs**")
            h9.markdown("**Monto**")

            if df_pagina.empty:
                st.info("No se encontraron resultados con los filtros seleccionados.")

            for _, row in df_pagina.iterrows():
                col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 3, 3, 2, 2, 2, 2, 2])

                col5.markdown(
                    f"[{row['cuit']}](https://lanus.infratrack.com.ar/legales?documento={row['cuit']})"
                    if row['cuit'] and row['cuit'] != "nan" else "N/A"
                )

                col2.markdown(
                    f"[{row['acta_numero']}](https://lanus.infratrack.com.ar/actas/{row['acta_numero']})"
                )
                col3.write(f"**{row.get("nombre_x", row.get("nombre", ""))}**")
                col7.write(f"Juzgado **{row["juzgado"]}**")
                col4.write(f":orange-badge[**{row["estado"]}**]")
                col6.write(f"**{row["fecha_infraccion"]}**")
                col8.write(f"**{row["ufs"]}**")
                col9.write(f"**${row["monto"]}**")

                st.divider()

        col_pag_1, col_pag_2, col_pag_3 = st.columns([1, 2, 1])

        with col_pag_1:
            if st.button(
                    "Anterior",
                    disabled=st.session_state.pagina_lotes <= 1,
                    icon=":material/keyboard_double_arrow_left:",
                    type="primary"
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
                    "Siguiente",
                    disabled=st.session_state.pagina_lotes >= total_paginas,
                    icon=":material/keyboard_double_arrow_right:",
                    type="primary"
            ):
                st.session_state.pagina_lotes += 1
                st.rerun()

    style_metric_cards(background_color="white", border_left_color="#b30000", box_shadow=False,
                       border_color="azure",
                       border_radius_px=30)
