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
    dataframe = dataframe.rename(columns={"cantidad": "Actas Pagadas"})
    return dataframe.sort_values(by="total", ascending=False).reset_index(drop=True)


def clean_camera_activity(dataframe):
    coordenadas = {
        "25 de Mayo y Av. San Martín (hacia el este)": (-34.704468687353426, -58.41562822567437),
        "25 de Mayo y Doctor Arturo Melo": (-34.7079843642299, -58.39438923283408),
        "29 de Septiembre y Cordero 1 (Norte)": (-34.73407779366845, -58.390095135997804),
        "29 de Septiembre y Cordero 2 (Sur)": (-34.73407558890403, -58.39018031586555),
        "29 de Septiembre y Esquiú": (-34.72540395446682, -58.390253004371125),
        "Avenida Hipolito Yrigoyen 2817 Sent.Asc": (-34.68915911920905, -58.38850504530596),
        "Avenida Hipolito Yrigoyen 2868 Sent.Desc": (-34.68935178526535, -58.388241896823885),
        "Avenida Hipolito Yrigoyen 6533 Sent.Asc.": (-34.73117173759956, -58.39676687704781),
        "Avenida Hipolito Yrigoyen 6576 Sent.Desc": (-34.73154539097939, -58.39649189455704),
        "Av. Hipólito Yrigoyen & De la Cruz": (-34.720873454341216, -58.39435085063931),
        "Av. Hipólito Yrigoyen & Fray Luis Beltrán": (-34.46867005729199, -58.64986840209329),
        "Av. Hipólito Yrigoyen & Raúl Alfonsín": (-34.692018145521864, -58.389392566186004),
        "Av. Pres. Hipólito Yrigoyen y O'Higgins": (-34.712635744929536, -58.392602745371576),
        "Av. Presidente Bernardino Rivadavia y Av. Remedios de Escalada de San Martín": (-34.67951043723301,
                                                                                         -58.404529971541194),
        "Av. Pres. Yrigoyen e Int. Manuel Quindimil": (-34.69824457721409, -58.39201988954947),
        "Av. Pte. Hipolito Yrigoyen y Av. Remedios de Escalada de San Martín": (-34.691853442775056,
                                                                                -58.389404331878694),
        "Av. Pte. Hipólito Yrigoyen y Riobamba": (-34.702321644706025, -58.39195414537197),
        "Av. San Martín y Viamonte (hacia el sur)": (-34.69598869163116, -58.4083227200902),
        "Gobernador Bernardo de Irigoyen & Avenida Hipólito Yrigoyen": (-34.70556637575157, -58.39172213877837),
        "Presidente Raul Alfonsin y General Madariaga": (-34.70677473503059, -58.37119323604923),
        "Pte. Alfonsín y Sarmiento": (-34.698944242443524, -58.380147028654804),
        "Remedios de Escalada y Pte. Perón": (-34.66457290433315, -58.417492918386145),
        "San Martín y Aristóbulo del Valle": (-34.70334132671643, -58.41475711653657),
        "San Martín y Remedios de Escalada": (-34.67797137761728, -58.406034168438936),
    }
    dataframe["latitud"] = dataframe["instalacion"].map(lambda x: coordenadas.get(x, (None, None))[0])
    dataframe["longitud"] = dataframe["instalacion"].map(lambda x: coordenadas.get(x, (None, None))[1])
    dataframe["cant"] = dataframe["cant"].astype(int)
    return dataframe
