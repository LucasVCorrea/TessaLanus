import pandas as pd

from ExtraFunctions.extras import normalizar_localidad


def get_tipos_notificaciones():
    tipos_infraccion = {
        "F": "Fotomulta",
        "V": "Velocidad",
        "CM": "Camara movil",
        "P": "PDA"
    }
    return tipos_infraccion


def clean_payments_data(dataframe):
    dataframe["fecha_acreditacion"] = pd.to_datetime(
        dataframe["fecha_acreditacion"],
    )
    dataframe["Tipo infraccion"] = dataframe["numero"].map(lambda x: x.split("-")[0]).map(get_tipos_notificaciones())
    dataframe["total"] = dataframe["total"].astype(int)
    return dataframe


def clean_notifications_data(dataframe):
    dataframe["Fecha Lote"] = pd.to_datetime(
        dataframe["Fecha Lote"],
    )
    dataframe["Tipo infraccion"] = dataframe["acta"].map(lambda x: x.split("-")[0]).map(get_tipos_notificaciones())
    dataframe["localidad"] = dataframe["localidad"].apply(normalizar_localidad)
    return dataframe
