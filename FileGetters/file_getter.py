import pandas as pd

from ExtraFunctions.file_parser import clean_notifications_data, clean_payments_data


def get_actas_pagadas_dataframe(csv_path="Files/Detalle de actas  Pagas-Lanus.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df = clean_payments_data(df)
        return df
    except FileNotFoundError:
        return pd.DataFrame()


def get_notificaciones_dataframe(csv_path="Files/Listado de actas notificadas-Lanus.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df = clean_notifications_data(df)
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
