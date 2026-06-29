import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from FileGetters.file_getter import get_ranking_medios_de_pago


def raised_by_type(dataframe):
    raised_by_type_grouop = dataframe.groupby("Tipo infraccion").agg({"total": ["sum"]}).reset_index()
    raised_by_type_grouop.columns = ["Tipo infraccion", "total"]
    fig = px.pie(raised_by_type_grouop, names="Tipo infraccion", values="total",
                 color_discrete_sequence=["#ff3333", "#6600ff", "#00e6ac", "yellow", 'deeppink']
                 , category_orders={"Tipo infraccion": ["Fotomulta",
                                                        "Velocidad",
                                                        "PDA",
                                                        "Camara movil"]}
                 )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        yaxis=dict(
            title=dict(font=dict(color='black'), ),
            tickfont=dict(color='black'),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        height=400,
    )
    fig.update_traces(
        textfont_size=16,

    )
    return fig


def notificated_by_location(dataframe):
    notificated_by_grouop = dataframe.groupby("localidad").agg({"lote_id": ["count"]}).reset_index()
    notificated_by_grouop.columns = ["Localidad", "Notificadas"]
    fig = px.pie(notificated_by_grouop.nlargest(5, "Notificadas"), names="Localidad", values="Notificadas",
                 color_discrete_sequence=["#0066ff", "#ff0066", "#ffa31a", "#ff00bf", "#1affa3"])
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        yaxis=dict(
            title=dict(font=dict(color='black'), ),
            tickfont=dict(color='black'),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        height=400,
    )
    fig.update_traces(
        textfont_size=16,

    )
    return fig


def daily_payments_by_type(dataframe):
    daily_payments_by_type_grouop = dataframe.groupby("fecha_acreditacion").agg(
        {"numero": ["count"]}).reset_index()
    daily_payments_by_type_grouop.columns = ["Fecha", "Actas Acreditadas"]
    # daily_payments_by_type_grouop["total"] = daily_payments_by_type_grouop["total"].map(lambda x:round(int(x)))
    fig = px.bar(daily_payments_by_type_grouop, x="Fecha", y="Actas Acreditadas",
                 color_discrete_sequence=["#ff3333", "MidnightBlue", "Red"], text_auto=True,
                 )
    fig.update_layout(

        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        yaxis=dict(
            title=dict(font=dict(color='black'), ),
            tickfont=dict(color='black'),
        ),
        barcornerradius=8,
        height=435,

    )
    fig.update_traces(textposition='inside', textfont_size=14)
    return fig


def tablero_heatmap(dataframe):
    agrupado = dataframe.groupby(["fecha_acreditacion", "Tipo infraccion"]).agg(
        {"numero": ["nunique"]}).reset_index()
    agrupado.columns = ["Fecha pago", "Tipo infraccion", "Total recaudado"]
    agrupado["Fecha pago"] = agrupado["Fecha pago"].dt.strftime("%d/%m/%Y")

    agrupado_pivot = agrupado.pivot_table(index="Fecha pago", columns="Tipo infraccion", values="Total recaudado").T

    z_raw = agrupado_pivot.values
    z = np.where(np.isnan(z_raw), -1, z_raw)

    text = np.where(np.isnan(z_raw), "", np.round(z_raw, 0).astype(int).astype(str))

    x = agrupado_pivot.columns.astype(str)
    y = agrupado_pivot.index.astype(str)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        text=text,
        texttemplate="%{text}",
        hovertemplate="Fecha: %{x}<br>Auditor: %{y}<br>Semáforos: %{z}<extra></extra>",
        xgap=0.5,
        ygap=0.5,
        colorbar=dict(
            title=dict(text="Actas pagadas en periodo", font=dict(color="black")),
            tickfont=dict(color="black")
        ),
        colorscale=px.colors.sequential.RdPu
    ))

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Tipo de Infraccion",
        xaxis_tickangle=-45,
        xaxis=dict(
            type="category",
            tickfont=dict(color="black"),
        ),
        yaxis=dict(
            type="category",
            tickfont=dict(color="black"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=60, b=20),

        title={
            'text': f"Cantidad de actas pagadas entre el {dataframe['fecha_acreditacion'].min().strftime('%d/%m/%Y')}"
                    f"y el {dataframe['fecha_acreditacion'].max().strftime('%d/%m/%Y')}",
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(color='black')
        },
        legend_title_font=dict(color='black')
    )
    fig.update_traces(textfont=dict(size=13))
    return fig


def show_ranking_medios_de_pago(dataframe):
    ranking = dataframe.groupby("Medio Pago").agg({"total": ["sum"]}).reset_index()

    ranking.columns = ["Medio pago", "total"]
    fig = px.pie(ranking.sort_values(by="total", ascending=False), values="total", names="Medio pago",
                 color="Medio pago", color_discrete_sequence=px.colors.qualitative.Set2, hole=.5)
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        yaxis=dict(
            title=dict(font=dict(color='black'), ),
            tickfont=dict(color='black'),
        ),

        height=350,
    )
    fig.update_traces(textposition='inside', textfont_size=14)
    return fig


def show_camera_map(df):
    df_mapa = df.copy()

    df_mapa = df_mapa.dropna(subset=["latitud", "longitud"])

    fig = px.scatter_mapbox(
        df_mapa,
        lat="latitud",
        lon="longitud",
        size="cant",
        color="cant",
        hover_name="instalacion",
        hover_data={
            "cant": True,
            "importe_final": True,
            "latitud": False,
            "longitud": False,
        },
        zoom=12,
        height=750,
        size_max=90,
        color_continuous_scale="Solar"
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},

        mapbox=dict(
            center=dict(
                lat=-34.70,
                lon=-58.40
            ),
            zoom=12,
        )
    )

    fig.update_traces(
        marker=dict(opacity=0.85)
    )

    return fig


def barplot_by_type(df):
    agrupado = df.groupby(["fecha_acreditacion", "Tipo infraccion"]).agg({"numero": ["count"]}).reset_index()
    agrupado.columns = ["fecha", "tipo", "acta"]
    fig = px.bar(agrupado, color="tipo", x="fecha", y="acta",
                 color_discrete_sequence=["#ff3333", "#6600ff", "#00e6ac", "yellow", "deeppink"]
                 , category_orders={"tipo": ["Fotomulta",
                                             "Velocidad",
                                             "PDA",
                                             "Camara movil"]},
                 text_auto=True)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        yaxis=dict(
            title=dict(font=dict(color='black'), ),
            tickfont=dict(color='black'),
        ),
        height=320)
    return fig


def ranking_pagos_plot(df):
    fig = px.pie(df, names="Medio Pago", values="total", color="Medio Pago",
                 color_discrete_sequence=["#0066ff", "#ff0066", "#ffa31a", "#ff1a1a", "#1affa3"], hole=.5)
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        yaxis=dict(
            title=dict(font=dict(color='black'), ),
            tickfont=dict(color='black'),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        height=400,
    )
    fig.update_traces(
        textfont_size=16,

    )
    return fig


def daily_notifications_plot(df):
    df["Fecha Lote"] = df["Fecha Lote"].dt.date
    if df["localidad"].nunique() < 4:
        agrupado = df.groupby(["Fecha Lote", "localidad"]).agg({"acta_id": ["count"]}).reset_index()
        agrupado.columns = ["Fecha", "Localidad", "Notificaciones"]
        agrupado["Notificaciones"] = agrupado["Notificaciones"].astype(int)
        fig = px.bar(agrupado, x="Fecha", y="Notificaciones", text_auto=True, color="Localidad",
                     color_discrete_sequence=["#ff3333", "#6600ff", "#00e6ac"])
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color='black'),
            xaxis=dict(
                title=dict(font=dict(color='black')),
                tickfont=dict(color='black'),
            ),
            yaxis=dict(
                title=dict(font=dict(color='black'), ),
                tickfont=dict(color='black'),
            ),
            barcornerradius=8,
            height=335,

        )
        fig.update_traces(textposition='inside', textfont_size=14)
    else:
        agrupado = df.groupby(["Fecha Lote", "localidad"]).agg({"acta_id": ["count"]}).reset_index()
        agrupado.columns = ["Fecha", "Localidad", "Notificaciones"]
        agrupado = agrupado.pivot_table(index="Fecha", columns="Localidad", values="Notificaciones").T
        data_pivot = agrupado.sort_index(ascending=False)

        z_raw = data_pivot.values
        z = np.where(np.isnan(z_raw), -1, z_raw)  # NaNs se marcan con -1 para identificar visualmente

        text = np.where(np.isnan(z_raw), "", np.round(z_raw, 0).astype(int).astype(str))

        x = data_pivot.columns.astype(str)
        y = data_pivot.index.astype(str)

        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale=px.colors.sequential.Reds,
            text=text,
            texttemplate="%{text}",
            hovertemplate="Fecha: %{x}<br>Localidad: %{y}<br>Notificaciones: %{z}<extra></extra>",
            xgap=0.5,
            ygap=0.5,
            colorbar=dict(
                title=dict(text="Actas Notificadas", font=dict(color="black")),
                tickfont=dict(color="black")
            )
        ))

        fig.update_layout(
            xaxis_title="Fecha",
            yaxis_title="Localidad",
            xaxis_tickangle=-45,
            xaxis=dict(
                type="category",
                tickfont=dict(color="black"),
            ),
            yaxis=dict(
                type="category",
                tickfont=dict(color="black"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=60, b=20),
        )
        fig.update_traces(textfont=dict(size=13))
    return fig


def barplot_diario_por_revisor(berisso_nivel_5):
    aceptadas_rechazadas_diario = (
        berisso_nivel_5
        .groupby(["Fecha", "Auditor"])
        .agg({"Aceptadas": "sum", "Rechazadas": "sum"})
        .reset_index()
    )

    df_melted = pd.melt(
        aceptadas_rechazadas_diario,
        id_vars=["Fecha", "Auditor"],
        var_name="Resultado",
        value_name="Presunciones de Nivel 5"
    )

    hover_info = (
        df_melted.groupby(["Fecha", "Resultado"])
        .apply(lambda g: "<br>".join([
            f"- {g.name[1]} {row['Auditor']}: {row['Presunciones de Nivel 5']}"
            for _, row in g.iterrows()
        ]))
        .reset_index(name="hover_text")
    )

    df_sum = (
        df_melted.groupby(["Fecha", "Resultado"], as_index=False)
        ["Presunciones de Nivel 5"].sum()
        .merge(hover_info, on=["Fecha", "Resultado"])
    )

    df_sum["Total de la fecha"] = (
        df_sum.groupby("Fecha")["Presunciones de Nivel 5"].transform("sum")
    )

    fig = px.bar(
        df_sum,
        x="Fecha",
        y="Presunciones de Nivel 5",
        color="Resultado",
        text_auto=True,
        hover_data={"hover_text": True, "Presunciones de Nivel 5": True},
        color_discrete_sequence=["Crimson", "#3333ff"]
    )

    fig.update_traces(
        hovertemplate="%{customdata[0]}<extra></extra>"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        yaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        barcornerradius=8,
        annotations=[
            dict(
                x=fecha,
                y=total,
                text=f"Total: {total}",
                showarrow=False,
                yshift=30,
                font=dict(color="black", size=12)
            )
            for fecha, total in (
                df_sum.groupby("Fecha")["Presunciones de Nivel 5"].sum().items()
            )
        ]
    )
    return fig


def grilla_revisores_nivel_5(berisso_nivel_5, fecha_desde, fecha_hasta):
    heatmap_auditor_nivel5 = (
        berisso_nivel_5
        .groupby(["Fecha", "Auditor"])
        .agg({"Total": ["sum"]})
        .reset_index()
    )
    heatmap_auditor_nivel5.columns = ["Fecha", "Auditor", "Total"]
    heatmap_auditor_nivel5["Fecha"] = pd.to_datetime(heatmap_auditor_nivel5["Fecha"]).dt.date

    pivot = heatmap_auditor_nivel5.pivot_table(
        index="Fecha",
        columns="Auditor",
        values="Total"
    ).fillna(-1)

    z = np.where(pivot.T.values == "No registró", -1, pivot.T.values.astype(float))
    text = np.where(z == -1, "No registró", np.round(z, 2).astype(str))

    x = pivot.index.astype(str)
    y = pivot.columns.astype(str)

    zmin, zmax = -1, np.nanmax(z)
    base_scale = px.colors.sequential.Reds
    colorscale = [[0.0, "darkgray"], [0.001, base_scale[0]]]
    for i, c in enumerate(base_scale):
        colorscale.append([(i + 1) / len(base_scale), c])

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale=colorscale,
        zmin=zmin,
        zmax=zmax,
        text=text,
        texttemplate="%{text}",
        hovertemplate="<b>Fecha: %{x}</b><br>Auditor: %{y}<br>Total: %{z}<extra></extra>",
        xgap=1,
        ygap=1,
        colorbar=dict(title="Presunciones Revisadas<br>Nivel 5")
    ))

    fig.update_layout(
        title=f"Actividad de Revisores Nivel 5 desde {fecha_desde} al {fecha_hasta}",
        xaxis_title="Fecha",
        yaxis_title="Revisor de Nivel 5",
        xaxis_tickangle=-45,
        xaxis=dict(type="category"),
        yaxis=dict(type="category"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color='black')
    )
    return fig


def show_camera_activity(dataframe_nivel_5_berisso):
    camera_activity = dataframe_nivel_5_berisso.groupby(["Fecha", "Código de cámara"]).agg(
        {"Aceptadas": ["sum"],
         "Rechazadas": ["sum"]}).reset_index()
    camera_activity.columns = ["Fecha", "Ubicacion", "Aceptadas", "Rechazadas"]
    camera_activity["Total"] = camera_activity["Aceptadas"] + camera_activity["Rechazadas"]
    fig = px.bar(camera_activity, x="Fecha", y="Aceptadas", color="Ubicacion", text_auto=True,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color='black'),
        xaxis=dict(
            title=dict(font=dict(color='black')),
            tickfont=dict(color='black'),
        ),
        yaxis=dict(
            title=dict(font=dict(color='black'), ),
            tickfont=dict(color='black'),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        height=490,
        barcornerradius=8

    )
    fig.update_traces(
        textfont_size=12,
    )
    return fig


def notifications_by_type(dataframe):
    notifications = (
        dataframe
        .groupby("notific_type")
        .agg({"acta_id": "nunique"})
        .reset_index()
    )

    notifications.columns = [
        "Tipo de Notificacion",
        "Actas notificadas"
    ]

    total = notifications["Actas notificadas"].sum()

    fig = px.pie(
        notifications,
        names="Tipo de Notificacion",
        values="Actas notificadas",
        color_discrete_sequence=[
            "crimson",
            "orange",
            "#ff3399",
            "#ff8533",
            "#ffff33"
        ],
        hole=0.6,
        category_orders={"Tipo de Notificacion": ["Email", "Bajo Puerta"]}
    )

    # TEXTO CENTRADO
    fig.add_annotation(
        text=f"<b>{total}</b><br>entregadas",
        x=0.5,
        y=0.5,
        font=dict(size=22, color="black"),
        showarrow=False
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        height=350,
    )

    fig.update_traces(
        textfont_size=12,
    )

    return fig


def activity_by_judge(dataframe):
    actividad = dataframe["juzgado"].value_counts().reset_index()
    actividad.columns = ["Juzgado", "Fallos Emitidos"]
    fig = px.pie(actividad, names="Juzgado", values="Fallos Emitidos",
                 color_discrete_sequence=["#0066ff", "#ff0066", "#ffa31a", "#ff00bf", "#1affa3"],
                 category_orders={"Juzgado": sorted(actividad["Juzgado"].unique().tolist())})
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        # height=350,
    )

    fig.update_traces(
        # textfont_size=12,
    )
    return fig


def daily_activity_judge(dataframe):
    dataframe["Fecha"] = dataframe["Fecha"].dt.date
    actividad_diaria = dataframe.groupby(["Fecha", "juzgado"]).agg({"acta": "count"}).reset_index()
    actividad_diaria.columns = ["Fecha", "Juzgado", "Fallos Emitidos"]
    fig = px.bar(actividad_diaria, x="Fecha", y="Fallos Emitidos", color="Juzgado",
                 color_discrete_sequence=["#0066ff", "#ff0066", "#ffa31a", "#ff00bf", "#1affa3"], text_auto=True,
                 category_orders={"Juzgado": sorted(actividad_diaria["Juzgado"].unique().tolist())})
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        height=450,
    )

    fig.update_traces(
        textfont_size=12,
    )
    return fig
