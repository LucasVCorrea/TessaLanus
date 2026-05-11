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


def clean_medios_de_pago(dataframe):
    dataframe["total"] = (
        dataframe["total"]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
        .astype(int)
    )

    dataframe["Monto ingresado"] = "$ " + dataframe["total"].map("{:,.0f}".format)

    dataframe["Monto ingresado"] = dataframe["Monto ingresado"].str.replace(",", ".")
    dataframe = dataframe.rename(columns={"cantidad":"Actas Pagadas"})
    return dataframe.sort_values(by = "total", ascending=False).reset_index(drop=True)
