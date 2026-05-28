import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from FileGetters.file_getter import get_ranking_medios_de_pago


def raised_by_type(dataframe):
    raised_by_type_grouop = dataframe.groupby("Tipo infraccion").agg({"total": ["sum"]}).reset_index()
    raised_by_type_grouop.columns = ["Tipo infraccion", "total"]
    fig = px.pie(raised_by_type_grouop, names="Tipo infraccion", values="total",
                 color_discrete_sequence=["Crimson", "#3333cc", "#00ff99", "yellow"]
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
                 color_discrete_sequence=["#e60000", "#bf4040", "#ff0080", "#751aff", "#ffff1a"])
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
                 color_discrete_sequence=["#b30000", "MidnightBlue", "Red"], text_auto=True,
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
                 color_discrete_sequence=["Crimson", "#3333cc", "#00ff99", "yellow"]
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
                 color_discrete_sequence=px.colors.qualitative.Set2, hole=.5)
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
                     color_discrete_sequence=["#b30000", "MidnightBlue", "yellow"])
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
