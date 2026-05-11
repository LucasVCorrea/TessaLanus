import streamlit as st

from FileGetters.file_getter import get_camaras_dataframe


def show_camera_activity():
    dataframe = get_camaras_dataframe()
    st.dataframe(dataframe)