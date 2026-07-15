import csv
import os
from datetime import datetime

import pandas as pd
import streamlit as st
def get_meses_ordenados():
    return ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
            "Noviembre", "Diciembre"]


def traducir_mes(mes):
    traduccion = {
        "January": "Enero",
        "February": "Febrero",
        "March": "Marzo",
        "April": "Abril",
        "May": "Mayo",
        "June": "Junio",
        "July": "Julio",
        "August": "Agosto",
        "September": "Septiembre",
        "October": "Octubre",
        "November": "Noviembre",
        "December": "Diciembre"
    }
    if pd.isna(mes):
        return "Mes desconocido"
    return traduccion.get(mes, "Mes desconocido")


def formatear_numero(n):
    if n < 1000:
        return str(n)
    elif n < 1_000_000:
        return f"{n / 1000:.1f}K"
    else:
        return f"{n / 1_000_000:.1f}M"


def semana_del_mes(fecha):
    dia_del_mes = fecha.day

    if 1 <= dia_del_mes <= 7:
        return 1
    elif 8 <= dia_del_mes <= 15:
        return 2
    elif 16 <= dia_del_mes <= 23:
        return 3
    elif 24 <= dia_del_mes <= 31:
        return 4
    return None


def get_mes_anterior(df, anio_actual, mes_dado):
    meses = get_meses_ordenados()
    idx = meses.index(mes_dado)

    # Caso normal (no es Enero)
    if idx > 0:
        mes_anterior = meses[idx - 1]
        return df[(df['Año'] == anio_actual) & (df['Mes'] == mes_anterior)]

    # Caso especial: Enero → Diciembre del año anterior
    else:
        anio_anterior = anio_actual - 1
        return df[(df['Año'] == anio_anterior) & (df['Mes'] == 'Diciembre')]


def de_mes_a_numero(mes):
    traduccion = {
        "01": "enero",
        "02": "febrero",
        "03": "marzo",
        "04": "abril",
        "05": "mayo",
        "06": "junio",
        "07": "julio",
        "08": "agosto",
        "09": "septiembre",
        "10": "octubre",
        "11": "noviembre",
        "12": "diciembre",
    }
    return traduccion[mes]


def get_actas_pagadas_csv():
    data_frame = pd.read_csv("Files/Detalle de actas pagas.csv")
    data_frame = clean_actas_pagadas(data_frame)
    return data_frame


def get_actas_notificadas():
    dataframe = pd.read_csv("Files/Actas enviadas al correo.csv")
    dataframe = clean_actas_notificadas(dataframe)
    return dataframe


def get_detalle_valores_infracciones():
    dataframe = pd.read_excel("Files/detalles_de_infracciones.xlsx")
    dataframe = clean_detalle_valores_infracciones(dataframe)
    return dataframe


def get_actas_tipo_infracciones():
    dataframe = pd.read_csv("Files/Actas por Tipo de Infraccion.csv")
    dataframe = clean_actas_tipo_infracciones(dataframe)
    return dataframe


def get_info_actas_total():
    dataframe = clean_merge_infracciones(get_actas_tipo_infracciones(), get_detalle_valores_infracciones())
    return dataframe


def get_fallos():
    dataframe = pd.read_csv("Files/Fallos.csv")
    dataframe = clean_fallos(dataframe)
    return dataframe


def clean_actas_pagadas(dataframe):
    dataframe["Mes"] = pd.to_datetime(dataframe["fecha_acreditacion"]).dt.month_name().str.capitalize()
    dataframe["Mes"] = dataframe["Mes"].map(traducir_mes)
    dataframe["fecha_pago"] = pd.to_datetime(dataframe["fecha_pago"])
    dataframe["created_at"] = pd.to_datetime(dataframe["created_at"])

    dataframe["Días transcurridos"] = (
            dataframe["fecha_pago"] - dataframe["created_at"]).dt.days
    dataframe["Fecha"] = pd.to_datetime(dataframe["fecha_acreditacion"]).dt.date

    dataframe.loc[:, 'Mes'] = pd.Categorical(dataframe['Mes'], categories=get_meses_ordenados(), ordered=True)
    dataframe = dataframe.sort_values(by="lote_id", na_position="last").drop_duplicates(subset="numero", keep="first")
    dataframe["Año"] = pd.to_datetime(dataframe["fecha_acreditacion"]).dt.year
    dataframe = dataframe.sort_values(by=['Mes'])
    return dataframe.loc[dataframe["Año"] >= 2024]


def clean_detalle_valores_infracciones(dataframe):
    dataframe["Año"] = dataframe["Año"].replace("", pd.NA).ffill()

    dataframe["Mes"] = dataframe["Mes"].str.title()

    nueva_fila = {'Año': 2025, 'Mes': "Enero", "Tipo de Faltas": "Invasion de senda", "Con Pago Voluntario": 50,
                  "Sin Pago Voluntario": 100, "Valor de la UF en 0": 1398, "Total con pago voluntario": 50 * 1398,
                  "Total sin pago voluntario": 100 * 1398
        , "Gastos administrativos": 15080}
    dataframe.loc[len(dataframe)] = nueva_fila
    dataframe["Tipo de Faltas"] = dataframe["Tipo de Faltas"].map(
        lambda x: x.rstrip())
    return dataframe


def clean_actas_notificadas(dataframe):
    dataframe["Mes"] = dataframe["month"].map(lambda x: x.split("-")[-1]).map(de_mes_a_numero).str.capitalize()
    dataframe["Año"] = dataframe["month"].map(lambda x: x.split("-")[0]).astype(int)
    # dataframe = dataframe.loc[dataframe["Año"] == "2025"]
    dataframe.loc[:, 'Mes'] = pd.Categorical(dataframe['Mes'], categories=get_meses_ordenados(), ordered=True)
    dataframe = dataframe.sort_values(by=['Mes'])
    return dataframe


def clean_actas_tipo_infracciones(dataframe):
    dataframe = dataframe.rename(columns={
        "CruzarRojo": "Semáforo en rojo",
        "Sin Casco": "Manejo sin casco",
        "Senda Peatonal": "Invasion de senda",
        "Giro Rojo": "Giro a la izquierda",
        "Giro Indebido": "Giro a la izquierda"})

    dataframe["date"] = dataframe["date"].astype(str)
    dataframe["Año"] = dataframe["date"].map(lambda x: x.split("-")[0])
    dataframe["Mes"] = dataframe["date"].map(lambda x: x.split("-")[-1]).map(
        de_mes_a_numero)
    dataframe["Mes"] = dataframe["Mes"].str.title()
    dataframe["Año"] = dataframe["Año"].astype(int)
    dataframe = dataframe.loc[dataframe["Año"] >= 2025]
    melt_infracciones = dataframe.melt(id_vars=['ubicacion','Año', 'Mes'],
                                       value_vars=['Semáforo en rojo', 'Manejo sin casco',
                                                   'Giro a la izquierda',
                                                   'Invasion de senda', 'Semáforo en rojo'],
                                       var_name='Tipo de Faltas', value_name='Cantidad cometidas')
    return melt_infracciones


def clean_merge_infracciones(dataframe_valores, dataframe_tipo_infracciones):
    dataframe = pd.merge(dataframe_valores, dataframe_tipo_infracciones, on=["Año", "Mes", "Tipo de Faltas"])
    dataframe["Generado"] = dataframe["Cantidad cometidas"] * ((dataframe[
                                                                    "Valor de la UF en 0"] *
                                                                dataframe[
                                                                    "Sin Pago Voluntario"]) +
                                                               dataframe[
                                                                   "Gastos administrativos"])

    infracciones_detalle_final = dataframe.groupby(["ubicacion","Año", "Mes", "Tipo de Faltas"]).agg(
        {"Cantidad cometidas": ["sum"],
         "Generado": ["sum"]}).reset_index()
    infracciones_detalle_final.columns = ["ubicacion","Año", "Mes", "Tipo de Faltas", "Cantidad cometidas", "Generado"]

    infracciones_detalle_final["total del mes"] = infracciones_detalle_final.groupby("Mes").transform("sum")[
        "Cantidad cometidas"]

    infracciones_detalle_final["Representacion por tipo de faltas"] = (
            infracciones_detalle_final["Cantidad cometidas"] * 100 / infracciones_detalle_final["total del mes"])

    infracciones_detalle_final["Porcentaje str"] = (round(
        infracciones_detalle_final["Representacion por tipo de faltas"], 2).astype(str)) + "%"

    infracciones_detalle_final["Generado str"] = "$ " + (
        (infracciones_detalle_final["Generado"] / 1000000).astype(str)) + "M"

    infracciones_detalle_final['Mes'] = pd.Categorical(infracciones_detalle_final['Mes'],
                                                       categories=get_meses_ordenados(),
                                                       ordered=True)
    return infracciones_detalle_final


def clean_fallos(dataframe):
    dataframe["Mes"] = pd.to_datetime(dataframe["fecha_fallo"]).dt.month_name().map(traducir_mes)
    dataframe["Fecha"] = pd.to_datetime(dataframe["fecha_fallo"]).dt.date
    dataframe = dataframe.drop_duplicates(subset=["acta"], keep="first")

    dataframe["Semana"] = dataframe["Fecha"].map(semana_del_mes)
    dataframe["Mes"] = pd.to_datetime(dataframe["Fecha"]).dt.month_name().map(traducir_mes)
    return dataframe


def get_fallos_raw():
    dataframe = pd.read_csv("Files/Fallos.csv")
    dataframe["Fecha"] = pd.to_datetime(dataframe["fecha_fallo"]).dt.date.astype(str)
    dataframe["Mes"] = pd.to_datetime(dataframe["fecha_fallo"]).dt.month_name().map(traducir_mes)
    dataframe = dataframe.rename(columns={"fallo": "Fallo"})
    return dataframe


def get_data_recaudado_vs_perdido(fallos, actas_pagadas):
    fallos_merge = fallos.groupby("Fecha").agg(
        {"valor_inicial": ["sum"], "valor_actual": ["sum"], "acta": ["count"]}).reset_index()
    fallos_merge.columns = ["Fecha", "valor_inicial", "valor_actual", "Actas con fallos"]

    actas_recaudado_diario = actas_pagadas.groupby("Fecha").agg(
        {"Monto Total": ["sum"], "Acta": ["count"]}).reset_index()
    actas_recaudado_diario.columns = ["Fecha", "Recaudado", "Actas pagadas"]

    recaudado_vs_perdido = pd.merge(actas_recaudado_diario, fallos_merge, on="Fecha")
    recaudado_vs_perdido["Reducido por fallos"] = recaudado_vs_perdido["valor_inicial"] - recaudado_vs_perdido[
        "valor_actual"]
    recaudado_vs_perdido = pd.melt(recaudado_vs_perdido[["Fecha", "Recaudado", "Reducido por fallos"]], id_vars="Fecha")
    return recaudado_vs_perdido


def get_perdido_por_dia_general(dataframe):
    dataframe = dataframe.copy()
    dataframe["Fecha"] = dataframe["Fecha"].astype(str)

    perdido_por_dia_general = dataframe.groupby(["Fecha", "Fallo"]).agg({"Perdido": ["sum"]}).reset_index()
    perdido_por_dia_general.columns = ["Fecha", "Fallo", "Reducido"]
    return perdido_por_dia_general


def get_fallos_por_dia(dataframe):
    fallos_por_dia = dataframe.groupby(["Fecha", "Fallo", "juzgado_id"]).agg(
        {"Fallo": ["count"]}).unstack().reset_index().fillna(0)
    fallos_por_dia.columns = ["Fecha", "Fallo", "Emitidos en Juzgado 1", "Emitidos en Juzgado 2"]
    fallos_por_dia["Fallo"] = fallos_por_dia["Fallo"].replace(
        {"1 - RESOLUCION CONDENATORIA COMUN PRESENCIAL": "CONDENATORIA COMUN PRESENCIAL",
         "3 - RESOLUCION CONDENATORIA COMUN PRESENCIAL ATENUANTE": "COMUN PRESENCIAL ATENUANTE", }).map(
        lambda x: x.title())
    return fallos_por_dia


def get_perdido_por_dia_final(dataframe1, dataframe2):
    dataframe1 = get_perdido_por_dia_general(dataframe1)
    dataframe2 = get_fallos_por_dia(dataframe2)
    perdido_por_dia_general = pd.merge(dataframe1, dataframe2, on=["Fecha", "Fallo"])
    return perdido_por_dia_general


def registrar_historial_acceso(nombre, usuario, rol):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ruta_archivo = "logs/historial_accesos.csv"
    archivo_existe = os.path.exists(ruta_archivo)

    with open(ruta_archivo, mode='a', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        if not archivo_existe:
            escritor.writerow(
                ['Nombre', 'Usuario', 'Rol', 'Fecha y Hora'])
        escritor.writerow([nombre, usuario, rol, now])


def get_ingresos_usuarios():
    dataframe = pd.read_csv("logs/historial_accesos.csv")
    return dataframe


# @st.cache_data(show_spinner=False)
def get_actividad_revisores_nivel_5():
    dataframe = pd.read_csv("Files/Actividad_revisores_nivel_5.csv")
    dataframe = clean_actividad_revisores(dataframe)
    return dataframe


def get_actas_notificadas_dataframe():
    lotes = pd.read_csv("Files/Listado de actas notificadas.csv")
    lotes["Mes"] = pd.to_datetime(lotes["Fecha Lote"]).dt.month_name().map(traducir_mes)
    lotes["Fecha Lote"] = pd.to_datetime(lotes["Fecha Lote"])
    lotes["Año"] = pd.to_datetime(lotes["Fecha Lote"]).dt.year.astype(int)
    return lotes.loc[lotes["Año"] >= 2024]


def get_actas_pagadas_de_lote(anio):
    pagadas = get_actas_pagadas_csv()
    pagoss = pagadas.groupby("lote_id").agg({"numero": ["count"]}).reset_index()
    pagoss.columns = ["lote_id", "actas pagadas del lote"]

    lotess_dataframe = get_actas_notificadas_dataframe()
    lotess = lotess_dataframe.loc[lotess_dataframe["Año"] == anio].groupby("lote_id").agg(
        {"acta_id": ["count"]}).reset_index()
    lotess.columns = ["lote_id", "actas notificadas"]

    data_ = pd.merge(lotess, get_actas_notificadas_dataframe()[["lote_id", "Mes"]], on="lote_id").drop_duplicates()
    data_ = pd.merge(data_, pagoss, on="lote_id", how="outer").drop_duplicates()
    return data_


def clean_actividad_revisores(actividad_revisores):
    actividad_revisores = actividad_revisores.rename(columns={'Cliente': 'Municipio'})
    actividad_revisores = actividad_revisores.loc[actividad_revisores["Municipio"] == "Berisso"]
    actividad_revisores['Municipio'] = actividad_revisores['Municipio'].astype(str).str.capitalize()
    actividad_revisores["Tipo de Cámara"] = actividad_revisores["Tipo de Revisión"].str.strip()
    actividad_revisores['Tipo de Cámara'] = actividad_revisores['Tipo de Cámara'].replace(
        {'Single Review': 'Luces', 'Multiple Review': 'Semáforo', "Plate Finder": "Buscador de patentes"})
    actividad_revisores['Auditor'] = actividad_revisores['Auditor'].map(
        lambda x: ' '.join(str(x).split()).title() if isinstance(x, str) else x
    )

    actividad_revisores["Código de cámara"] = actividad_revisores["Código de cámara"].replace(
        {"4-C64 - Av 122 y calle 64": "4C64 - Av 122 y calle 64",
         "3-C59 - Av 122 y calle 59": "3C59 - Av 122 y calle 59",
         "5-C126 - Av 60 y calle 126": "5C126 - Av 60 y calle 126"})
    actividad_revisores['Código limpio'] = actividad_revisores['Código de cámara'].map(
        lambda x: str(x).split('-')[0].strip() if isinstance(x, str) else None
    )

    actividad_revisores['Código de cámara'] = actividad_revisores['Código de cámara'].map(
        lambda x: str(x).split('-')[-1].strip() if isinstance(x, str) else None
    )

    actividad_revisores['Fecha'] = pd.to_datetime(actividad_revisores['Fecha'])
    actividad_revisores['Año'] = actividad_revisores['Fecha'].dt.year
    actividad_revisores = actividad_revisores.sort_values(by='Fecha')
    actividad_revisores_listo = actividad_revisores.drop(
        columns=['Tipo de Revisión', '% aceptadas', 'Recorte', 'Deshacer', 'NoOp'])
    actividad_revisores_listo['Mes'] = actividad_revisores_listo['Fecha'].dt.month_name().map(traducir_mes)
    actividad_revisores_listo['Mes/Año'] = (
            actividad_revisores_listo['Fecha'].dt.month_name().map(traducir_mes)
            + "-" +
            actividad_revisores_listo["Año"].astype(str)
    )
    actividad_revisores_listo['Aceptadas'] = pd.to_numeric(actividad_revisores_listo['Aceptadas'], errors='coerce')
    actividad_revisores_listo['Rechazadas'] = pd.to_numeric(actividad_revisores_listo['Rechazadas'], errors='coerce')
    actividad_revisores_listo['Semana'] = actividad_revisores_listo['Fecha'].map(semana_del_mes)
    auditores_unlam = actividad_revisores_listo.loc[actividad_revisores_listo['Mes'] == 'Enero'][
        'Auditor'].unique().tolist()
    auditores_unlam += ['Miguel Gullo', 'Celeste Donato', 'Ramiro Odella', 'Yanina Denise Ybarra', 'Jeronimo Blanco']
    actividad_revisores_listo['Mes'] = pd.Categorical(
        actividad_revisores_listo['Mes'],
        categories=get_meses_ordenados(),
        ordered=True
    )
    actividad_revisores_listo = actividad_revisores_listo.sort_values(by="Mes", ascending=False)
    actividad_revisores_listo = actividad_revisores_listo.loc[actividad_revisores_listo["Municipio"] != "Ezeiza_ftl"]
    actividad_revisores_listo = actividad_revisores_listo.loc[
        actividad_revisores_listo["Tipo de Cámara"].isin(["Semáforo", "Luces", "Buscador de patentes"])]
    return actividad_revisores_listo.loc[
        ~actividad_revisores["Auditor"].isin(["Daniela Zarza", "Lucia Ferrero", "Romina Higa"])].loc[
        actividad_revisores_listo['Nivel de Revisión'] == 5].drop_duplicates()

# def to_excel_reporte(df):
#     output = io.BytesIO()
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         df.to_excel(writer, index=False, sheet_name='Reporte de cámaras')
#     processed_data = output.getvalue()
#     return processed_data
def get_ultima_actividad_usuarios():
    accesos = pd.read_csv("logs/historial_accesos.csv")

    accesos["dt_limpio"] = pd.to_datetime(
        accesos["Fecha y Hora"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    ) - pd.Timedelta(hours=3)

    accesos = accesos.dropna(subset=["dt_limpio"])

    # ⬇️ AGRUPAMOS POR USUARIO (NO POR NOMBRE)
    tabla = (
        accesos
        .sort_values("dt_limpio")
        .groupby("Usuario", as_index=False)
        .last()
    )

    # Fechas formateadas
    tabla["ultima_conex_fecha"] = tabla["dt_limpio"].dt.strftime("%d/%m/%Y")
    tabla["ultima_conex_hora"] = tabla["dt_limpio"].dt.strftime("%H:%M:%S")

    ahora = pd.Timestamp.now() - pd.Timedelta(hours=3)

    tabla["minutos_desde_ultima_conexion"] = (
            (ahora - tabla["dt_limpio"]).dt.total_seconds() // 60
    ).astype(int).clip(lower=0)

    tabla["dias_desde_ultima_conexion"] = (
            ahora.normalize() - tabla["dt_limpio"].dt.normalize()
    ).dt.days.astype(int)

    return (
        tabla
        .sort_values("minutos_desde_ultima_conexion")
        .head(20)
    )


# Esto en format:
@st.dialog("🕑 Ultimas 20 Conexiones")
def mostrar_ultima_conexion():
    st.write(
        ":green-badge[Conexión reciente] :orange-badge[2 ó más días sin conectarse] :red-badge[Tiempo sin conectarse]")
    tabla_de_accesos = get_ultima_actividad_usuarios()

    def texto_tiempo(row):
        minutos = row["minutos_desde_ultima_conexion"]
        dias = row["dias_desde_ultima_conexion"]

        if minutos < 1:
            return "recién conectado"

        if dias <= 1:
            if minutos < 60:
                return f"{minutos} mins"
            else:
                h = minutos // 60
                m = minutos % 60
                if m == 0:
                    return f"{h} hs"
                return f"{h} hs, {m} mins"
        else:
            return f"{dias} días"

    for _, row in tabla_de_accesos.iterrows():

        dias = row["dias_desde_ultima_conexion"]
        minutos = row["minutos_desde_ultima_conexion"]
        horas = minutos // 60
        rol = row["Rol"]

        if rol == "moderador":
            rol_badge_color = "violet"
        elif rol == "admin":
            rol_badge_color = "grey"
        else:
            rol_badge_color = "blue"
        # Badge
        if dias <= 2:
            badge_label = "Activo"
            badge_color = "green"
        elif dias <= 14:
            badge_label = "Inactivo rec."
            badge_color = "orange"
        else:
            badge_label = "Inactivo"
            badge_color = "red"

        tiempo_txt = texto_tiempo(row)

        st.write(
            f":{badge_color}-badge[:material/person: **{row['Nombre']}**] :{rol_badge_color}-badge[{row['Rol']}] Ult. conexión: "
            f"{row['ultima_conex_fecha']} {row['ultima_conex_hora']}"
            f"({tiempo_txt})"
        )