import pandas as pd

from ExtraFunctions.extras import normalizar_localidad
from format import traducir_mes


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
    dataframe["Año"] = dataframe["fecha_acreditacion"].dt.year
    dataframe["Mes"] = pd.to_datetime(dataframe["fecha_acreditacion"]).dt.month_name().str.capitalize()
    dataframe["Mes"] = dataframe["Mes"].map(traducir_mes)
    dataframe["Tipo infraccion"] = dataframe["numero"].map(lambda x: x.split("-")[0]).map(get_tipos_notificaciones())
    dataframe = dataframe.rename(columns={"Monto Total": "total"})
    dataframe["total"] = dataframe["total"].map(lambda x: x.replace(".", "")).map(lambda x: x.replace(",", ".")).astype(
        float)
    dataframe["Tasa administrativa"] = dataframe["Tasa administrativa"].map(lambda x: x.replace(".", "")).map(
        lambda x: x.replace(",", ".")).astype(
        float)
    dataframe["Tasa infraccion"] = dataframe["Tasa infraccion"].map(lambda x: x.replace(".", "")).map(
        lambda x: x.replace(",", ".")).astype(
        float)
    return dataframe.loc[dataframe["Tipo infraccion"] != "Otros"]


def clean_notifications_data(dataframe_bajo_puerta, dataframe_email):
    dataframe = pd.concat([dataframe_bajo_puerta, dataframe_email], ignore_index=True)
    dataframe["Fecha Lote"] = pd.to_datetime(
        dataframe["Fecha Lote"],
    )
    dataframe["Año"] = dataframe["Fecha Lote"].dt.year
    dataframe["Mes"] = pd.to_datetime(dataframe["Fecha Lote"]).dt.month_name().str.capitalize()
    dataframe["Mes"] = dataframe["Mes"].map(traducir_mes)
    # dataframe["Tipo infraccion"] = dataframe["acta"].map(lambda x: x.split("-")[0]).map(get_tipos_notificaciones())
    dataframe["localidad"] = dataframe["localidad"].apply(normalizar_localidad)
    dataframe["Mes_num"] = pd.to_datetime(
        dataframe["Fecha Lote"]
    ).dt.month

    return dataframe


def clean_medios_de_pago(dataframe):
    dataframe = dataframe.rename(columns={"Monto Total": "total"})
    dataframe["total"] = dataframe["total"].astype(str)
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


def clean_activity(dataframe):
    dataframe["Fecha"] = pd.to_datetime(
        dataframe["Fecha"],
    )
    dataframe["Año"] = dataframe["Fecha"].dt.year
    dataframe["Mes"] = pd.to_datetime(dataframe["Fecha"]).dt.month_name().str.capitalize()
    dataframe["Mes"] = dataframe["Mes"].map(traducir_mes)
    dataframe['Aceptadas'] = pd.to_numeric(dataframe['Aceptadas'], errors='coerce')
    dataframe['Rechazadas'] = pd.to_numeric(dataframe['Rechazadas'], errors='coerce')
    dataframe['Total'] = pd.to_numeric(dataframe['Total'], errors='coerce')

    return dataframe


def clean_fallos_judiciales(dataframe):
    dataframe["Fecha"] = pd.to_datetime(dataframe["fecha_fallo"], errors="coerce")

    dataframe["Año"] = dataframe["Fecha"].dt.year
    dataframe["Mes"] = dataframe["Fecha"].dt.month_name().str.capitalize()
    dataframe["Mes"] = dataframe["Mes"].map(traducir_mes)

    dataframe["fecha_fallo"] = dataframe["Fecha"].dt.date
    return dataframe


def clean_ranking_actualizado(dataframe):
    import unicodedata
    import re

    df = dataframe.copy()

    def limpiar(valor):
        if pd.isna(valor):
            return ""

        valor = str(valor).upper().strip()

        valor = (
            valor.replace("�", "")
            .replace("\xad", "")
            .replace("Ã³", "O")
            .replace("Ã©", "E")
            .replace("PIÃ±EIRO", "PIÑEIRO")
            .replace("º", "O")
            .replace("°", "O")
        )

        valor = unicodedata.normalize("NFKD", valor)
        valor = valor.encode("ASCII", "ignore").decode("utf-8")

        valor = re.sub(r"\bPARTIDO\b|\bPDO\b|\bPDTO\b|\bDPTO\b|\bPCIA\b", " ", valor)
        valor = re.sub(r"[_/*.,;:()?\-]+", " ", valor)
        valor = re.sub(r"\s+", " ", valor).strip()

        return valor

    def normalizar(valor):
        loc = limpiar(valor)

        if loc in ["", "NAN", "NONE", "NO CONSTA", "SIN INFORMAR", "NO DISPONIBLE", "---", "SA", "B"]:
            return ""

        if (
                (
                        "AUTONOMA" in loc
                        and (
                                "BS" in loc
                                or "BUENOS AIRES" in loc
                        )
                )
                or loc in [
            "CABA",
            "C A B A",
            "CAPITAL",
            "CAPITAL FEDERAL",
            "CIUDAD",
            "CIUDAD AUTONOMA",
        ]
                or loc.startswith("CABA COMUNA")
                or loc.startswith("COMUNA")
        ):
            return "CIUDAD AUTÓNOMA DE BUENOS AIRES"

        # LANÚS
        if "LANUS" in loc or "LANS" in loc or "LANUES" in loc or "LANU " in loc:
            if "OESTE" in loc or "OSTE" in loc or loc in ["LANUS O", "LANUS O LANUS", "LANS OESTE", "LANU OESTE"]:
                return "LANÚS OESTE"
            if "ESTE" in loc or loc in ["LANUS E", "LANU ESTE"]:
                return "LANÚS ESTE"
            if "VILLA DIAMANTE" in loc or "V DIAMANTE" in loc:
                return "VILLA DIAMANTE - LANÚS"
            if "VILLA CARAZA" in loc or "V CARAZA" in loc:
                return "VILLA CARAZA - LANÚS"
            if "V INDUSTRIALES" in loc or "VILLA INDUSTRIALES" in loc or "VILLA DE LOS INDUSTRIALES" in loc:
                return "VILLA DE LOS INDUSTRIALES - LANÚS"
            if "MONTE CHINGOLO" in loc or "MTE CHINGOLO" in loc:
                return "MONTE CHINGOLO - LANÚS"
            if "VALENTIN ALSINA" in loc or "V ALSINA" in loc:
                return "VALENTÍN ALSINA - LANÚS"
            if "ESCALADA" in loc:
                return "REMEDIOS DE ESCALADA - LANÚS"
            return "LANÚS"

        # Remedios de Escalada
        if "ESCALADA" in loc or "RDIOS" in loc:
            return "REMEDIOS DE ESCALADA"

        # Valentín Alsina
        if "VALENT" in loc or loc in ["V ALSINA"]:
            return "VALENTÍN ALSINA"

        # Lomas de Zamora y localidades asociadas
        if "LOMAS" in loc or "L DE ZAMORA" in loc or "LDE ZAMORA" in loc:
            if "BANFIELD" in loc:
                return "BANFIELD - LOMAS DE ZAMORA"
            if "TEMPERLEY" in loc or "TEMPEREY" in loc or "TERMPERLEY" in loc:
                return "TEMPERLEY - LOMAS DE ZAMORA"
            if "LLAVALLOL" in loc or "LAVALLOL" in loc:
                return "LLAVALLOL - LOMAS DE ZAMORA"
            if "TURDERA" in loc:
                return "TURDERA - LOMAS DE ZAMORA"
            if "VILLA FIORITO" in loc or "V FIORITO" in loc:
                return "VILLA FIORITO - LOMAS DE ZAMORA"
            if "VILLA ALBERTINA" in loc or "V ALBERTINA" in loc:
                return "VILLA ALBERTINA - LOMAS DE ZAMORA"
            if "INGENIERO BUDGE" in loc or "ING BUDGE" in loc:
                return "INGENIERO BUDGE - LOMAS DE ZAMORA"
            return "LOMAS DE ZAMORA"

        # Almirante Brown
        if "ALTE BROWN" in loc or "ALMIRANTE BROWN" in loc or "A BROWN" in loc:
            if "ADROGUE" in loc:
                return "ADROGUÉ - ALMIRANTE BROWN"
            if "BURZACO" in loc:
                return "BURZACO - ALMIRANTE BROWN"
            if "GLEW" in loc:
                return "GLEW - ALMIRANTE BROWN"
            if "LONGCHAMPS" in loc or "LONCHAMPS" in loc:
                return "LONGCHAMPS - ALMIRANTE BROWN"
            if "RAFAEL CALZADA" in loc or "R CALZADA" in loc or loc == "CALZADA":
                return "RAFAEL CALZADA - ALMIRANTE BROWN"
            if "CLAYPOLE" in loc:
                return "CLAYPOLE - ALMIRANTE BROWN"
            if "JOSE MARMOL" in loc or "J MARMOL" in loc:
                return "JOSÉ MÁRMOL - ALMIRANTE BROWN"
            return "ALMIRANTE BROWN"

        # Avellaneda
        if "AVELLANEDA" in loc:
            if "PINEIRO" in loc or "PINEYRO" in loc or "PIEIRO" in loc or "PINIERO" in loc:
                return "PIÑEYRO - AVELLANEDA"
            if "SARANDI" in loc:
                return "SARANDÍ - AVELLANEDA"
            if "WILDE" in loc:
                return "WILDE - AVELLANEDA"
            if "GERLI" in loc:
                return "GERLI - AVELLANEDA"
            if "DOMINICO" in loc:
                return "VILLA DOMÍNICO - AVELLANEDA"
            if "DOCK SUD" in loc:
                return "DOCK SUD - AVELLANEDA"
            return "AVELLANEDA"

        # Correcciones exactas comunes
        exactos = {
            "ADROGUE": "ADROGUÉ",
            "ADROGU": "ADROGUÉ",
            "A KORN": "ALEJANDRO KORN",
            "JOSE MARMOL": "JOSÉ MÁRMOL",
            "J MARMOL": "JOSÉ MÁRMOL",
            "TRISTAN SUAREZ": "TRISTÁN SUÁREZ",
            "MORON": "MORÓN",
            "ITUZAINGO": "ITUZAINGÓ",
            "VTE LOPEZ": "VICENTE LÓPEZ",
            "VICENTE LOPEZ": "VICENTE LÓPEZ",
            "SAN JOSE": "SAN JOSÉ",
            "SAN CRISTOBAL": "SAN CRISTÓBAL",
            "LUIS GUILLON": "LUIS GUILLÓN",
            "EL JAGUEL": "EL JAGÜEL",
            "SARANDI": "SARANDÍ",
            "VILLA DOMINICO": "VILLA DOMÍNICO",
            "V DOMINICO": "VILLA DOMÍNICO",
            "VILLA DOMINICO AVELLANEDA": "VILLA DOMÍNICO - AVELLANEDA",
            "PINEIRO": "PIÑEYRO",
            "PINEYRO": "PIÑEYRO",
            "PINIERO": "PIÑEYRO",
            "PIEIRO": "PIÑEYRO",
            "PIEIIRO": "PIÑEYRO",
            "TEMPEREY": "TEMPERLEY",
            "TERMPERLEY": "TEMPERLEY",
            "BENFIELD": "BANFIELD",
            "BANDFIELD": "BANFIELD",
            "BAFIELD": "BANFIELD",
            "LAVALLOL": "LLAVALLOL",
            "LONCHAMPS": "LONGCHAMPS",
            "MTE GRANDE": "MONTE GRANDE",
            "MTE GDE": "MONTE GRANDE",
            "MTE CHINGOLO": "MONTE CHINGOLO",
            "MONTE CHINGOLO": "MONTE CHINGOLO",
            "SAN FCO SOLANO": "SAN FRANCISCO SOLANO",
            "S F SOLANO": "SAN FRANCISCO SOLANO",
            "S FCO SOLANO": "SAN FRANCISCO SOLANO",
            "FCIO VARELA": "FLORENCIO VARELA",
            "GDOR VIRASORO": "GOBERNADOR VIRASORO",
            "GRAL RODRIGUEZ": "GENERAL RODRÍGUEZ",
            "GENERAL RODRIGUEZ": "GENERAL RODRÍGUEZ",
            "SGO DEL ESTERO": "SANTIAGO DEL ESTERO",
            "LAPLATA": "LA PLATA",
            "PLATANOS": "PLÁTANOS",
            "OLVIOS": "OLIVOS",
            "CRUCESITA": "CRUCECITA",
            "GERLLI": "GERLI",
            "RNELAGH": "RANELAGH",
            "GOUDGE": "GUERNICA",
        }

        if loc in exactos:
            return exactos[loc]

        return loc.title()

    df["Localidad"] = df["Localidad"].apply(normalizar)

    return df.drop(columns = "Unnamed: 0")
