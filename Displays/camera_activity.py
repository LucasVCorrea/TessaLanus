import streamlit as st

from FileGetters.file_getter import get_camaras_dataframe
from Plots.get_plot import show_camera_map


def show_camera_activity():
    dataframe = get_camaras_dataframe()
    st.caption("**Actividad de Cámaras en 2026**")
    ver_mapa = st.toggle("Ver mapa")
    if ver_mapa:
        st.plotly_chart(
            show_camera_map(dataframe),
            width="stretch",
            config={
                "scrollZoom": True,
                "displayModeBar": True
            }
        )
    else:
        st.dataframe(dataframe.rename(columns={"instalacion": "Ubicacion",
                                               "cant": "Actas Generadas",
                                               "importe_final": "Recaudado"}).drop(
            columns=["latitud", "longitud"]).sort_values(by="Actas Generadas", ascending=True), hide_index=True)
