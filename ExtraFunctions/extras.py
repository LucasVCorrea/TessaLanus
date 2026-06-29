import io

import pandas as pd
import re
import unicodedata


def notifications_by_day(dataframe):
    agrupado_por_fecha = dataframe.groupby(["Fecha Lote"]).agg({"acta_id": ["count"]}).reset_index()
    agrupado_por_fecha.columns = ["Fecha Lote", "Cantidad"]
    return agrupado_por_fecha["Cantidad"].mean()


def normalizar_texto(texto):
    if pd.isna(texto):
        return None

    texto = str(texto).strip().upper()

    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

    texto = texto.replace("Ã©", "E")

    texto = re.sub(r"[\.\,\-\*\(\)]", " ", texto)

    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


equivalencias = {

    # ---------------- CABA ----------------
    "CABA": "CABA",
    "C A B A": "CABA",
    "C AUTONOMA DE BS AS": "CABA",
    "CIUDAD AUTONOMA": "CABA",
    "CIUDAD AUTONOMA DE BS AS": "CABA",
    "CIUDAD AUTONOMA DE BUENOS AIRES": "CABA",
    "CIUDAD DE BUENOS AIRES": "CABA",
    "CIUDAD AUTONOMA DE BUENOS AIRES ": "CABA",
    "CIUDAD AUTONOMA DE BS AS ": "CABA",
    "CDAD DE BS AS": "CABA",
    "CAPITAL FEDERAL": "CABA",
    "CPTAL FEDERAL": "CABA",
    "PALERMO": "CABA",
    "BARRACAS": "CABA",
    "LA BOCA": "CABA",

    # ---------------- LANUS ----------------
    "LANUS": "LANUS",
    "LANUS ESTE": "LANUS ESTE",
    "LANUS OESTE": "LANUS OESTE",
    "LANUS ESTE LANUS": "LANUS ESTE",
    "LANUS OESTE ": "LANUS OESTE",

    # ---------------- LOMAS ----------------
    "LOMAS DE ZAMORA": "LOMAS DE ZAMORA",
    "L DE ZAMORA": "LOMAS DE ZAMORA",
    "V FIORITO L DE ZAMORA": "VILLA FIORITO",

    # ---------------- FLORENCIO VARELA ----------------
    "FLORENCIO VARELA": "FLORENCIO VARELA",
    "FCIO VARELA": "FLORENCIO VARELA",
    "FCIO VARELA": "FLORENCIO VARELA",

    # ---------------- ADROGUE ----------------
    "ADROGUE": "ADROGUE",
    "ADROGUE ALTE BROWN": "ADROGUE",
    "ADROGUE ALMIRANTE BROWN": "ADROGUE",

    # ---------------- BURZACO ----------------
    "BURZACO": "BURZACO",
    "BURZACO ALTE BROWN": "BURZACO",
    "BURZACO ALMIRANTE BROWN": "BURZACO",

    # ---------------- LONGCHAMPS ----------------
    "LONGCHAMPS": "LONGCHAMPS",
    "LONGCHAMPS ALTE BROWN": "LONGCHAMPS",

    # ---------------- SARANDI ----------------
    "SARANDI": "SARANDI",
    "SARANDI AVELLANEDA": "SARANDI",
    "SARANDI PARTIDO AVELLANEDA": "SARANDI",
    "SARANDI PARTIDO DE AVELLANEDA": "SARANDI",
    "SARANDI DPTO AVELLANEDA": "SARANDI",

    # ---------------- AVELLANEDA ----------------
    "AVELLANEDA": "AVELLANEDA",
    "AVELLANEDA DPTO AVELLANEDA": "AVELLANEDA",

    # ---------------- WILDE ----------------
    "WILDE": "WILDE",
    "WILDE AVELLANEDA": "WILDE",
    "WILDE PDO AVELLANEDA": "WILDE",

    # ---------------- BERNAL ----------------
    "BERNAL": "BERNAL",
    "BERNAL QUILMES": "BERNAL",
    "BERNAL OESTE": "BERNAL OESTE",
    "BERNAL OESTE QUILMES": "BERNAL OESTE",

    # ---------------- QUILMES ----------------
    "QUILMES": "QUILMES",
    "QUILMES ESTE": "QUILMES ESTE",
    "QUILMES OESTE": "QUILMES OESTE",

    # ---------------- ALEJANDRO KORN ----------------
    "A KORN": "ALEJANDRO KORN",
    "A KORN SAN VICENTE": "ALEJANDRO KORN",
    "ALEJANDRO KORN": "ALEJANDRO KORN",
    "ALEJANDRO KORN SAN VICENTE": "ALEJANDRO KORN",

    # ---------------- REMEDIOS DE ESCALADA ----------------
    "R DE ESCALADA": "REMEDIOS DE ESCALADA",
    "REMEDIOS DE ESCALADA": "REMEDIOS DE ESCALADA",

    # ---------------- RAFAEL CALZADA ----------------
    "R CALZADA ALTE BROWN": "RAFAEL CALZADA",
    "RAFAEL CALZADA": "RAFAEL CALZADA",

    # ---------------- LA PLATA ----------------
    "LA PLATA": "LA PLATA",
    "LA PLATA BS AS": "LA PLATA",
    "LA PLATA ": "LA PLATA",
    "CITY BELL": "CITY BELL",
    "VILLA ELISA LA PLATA BS AS": "VILLA ELISA",

    # ---------------- OTROS ----------------
    "TEMPERLEY": "TEMPERLEY",
    "LLAVALLOL": "LLAVALLOL",
    "LUIS GUILLON": "LUIS GUILLON",
    "GERLI": "GERLI",
    "MONTE CHINGOLO": "MONTE CHINGOLO",
    "PIÑEYRO": "PIÑEIRO",
    "PINEYRO": "PIÑEIRO",
    "PINEIRO": "PIÑEIRO",
    "GUERNICA": "GUERNICA",
    "GUERNICA PTE PERON": "GUERNICA",
    "GLEW": "GLEW",
    "CLAYPOLE": "CLAYPOLE",
    "VILLA DOMINICO": "VILLA DOMINICO",
    "VILLA CELINA": "VILLA CELINA",
    "SAN JOSE": "SAN JOSE",
    "ING BUDGE": "INGENIERO BUDGE",
    "FLORIDA": "FLORIDA",
    "MAKALLE GRAL DONOVAN": "MAKALLE",

    # ---------------- VACIOS ----------------
    "": None,
    "NO DISPONIBLE": None,
}


def normalizar_localidad(valor):
    valor = normalizar_texto(valor)

    if valor is None:
        return None

    return equivalencias.get(valor, valor)

def to_excel_reporte(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte de cámaras')
    processed_data = output.getvalue()
    return processed_data

# def show_user_and_logout():
#
#     user = st.session_state.get("user", None)
#
#     if user is not None:
#         st.sidebar.write(f"**Usuario:** {user}")
#         if st.sidebar.button("Cerrar sesión"):
#             st.session_state["user"] = None
#             st.experimental_rerun()

def payed_notifications(notifcations_dataframe, payments_dataframe, how):
    payments_dataframe = payments_dataframe.rename(columns={"numero": "acta"})
    merged = pd.merge(notifcations_dataframe, payments_dataframe, on="acta", how = how)
    return merged.drop_duplicates(subset="acta", keep="first")
