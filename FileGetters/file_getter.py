import pandas as pd

from ExtraFunctions.file_parser import clean_notifications_data, clean_payments_data, clean_medios_de_pago, \
    clean_activity, clean_fallos_judiciales,clean_ranking_actualizado


def get_actas_pagadas_dataframe(csv_path="Files/Detalle de actas Pagas-Lanus.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df = clean_payments_data(df)
        return df
    except FileNotFoundError:
        return pd.DataFrame()


def get_notificaciones_dataframe(csv_path="Files/Listado de actas notificadas Lanus Bajo Puerta.csv",
                                 csv_path_2="Files/Listado de actas notificadas Lanus Email.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df["notific_type"] = "Bajo Puerta"

        df_2 = pd.read_csv(csv_path_2, dtype=str)
        df_2 = df_2.fillna("")
        df_2["notific_type"] = "Email"

        df = clean_notifications_data(df, df_2)
        return df
    except FileNotFoundError:
        return pd.DataFrame()


def get_valor_uf_dataframe(csv_path="Files/Valor historico UF.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        return df
    except FileNotFoundError:
        return pd.DataFrame()


def get_ranking_medios_de_pago(df):
    try:
        df = df.fillna("")
        df = clean_medios_de_pago(df)
        df = df.groupby("medio_pago").agg({"total": ["sum"]}).reset_index()
        df.columns = ["Medio Pago", "total"]
        return df.nlargest(5, "total")
    except FileNotFoundError:
        return pd.DataFrame()


def get_camaras_dataframe(csv_path="Files/Recaudacion por Camara-Lanus.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df = clean_camera_activity(df)
        return df
    except FileNotFoundError:
        return pd.DataFrame()


def get_actividad_nivel_5(csv_path="Files/actividad_nivel_5_lanus.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df = clean_activity(df)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def get_actas_a_preescribir(csv_path="Files/Actas preescribir.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def get_fallos_dataframe(csv_path="Files/Fallos-Juzgados.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df = clean_fallos_judiciales(df)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def get_ranking_actualizado(csv_path = "Files/Ranking_actualizado.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df = clean_ranking_actualizado(df)
        return df
    except FileNotFoundError:
        return pd.DataFrame()