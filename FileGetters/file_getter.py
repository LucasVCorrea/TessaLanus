import pandas as pd

from ExtraFunctions.file_parser import clean_notifications_data, clean_payments_data, clean_medios_de_pago, \
    clean_camera_activity


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


def get_ranking_medios_de_pago(csv_path="Files/Ranking Medios de Pagos-Lanus.csv"):
    try:
        df = pd.read_csv(csv_path, dtype=str)
        df = df.fillna("")
        df = clean_medios_de_pago(df)
        return df
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
