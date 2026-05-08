import plotly.express as px


def raised_by_type(dataframe):
    raised_by_type_grouop = dataframe.groupby("Tipo infraccion").agg({"total": ["sum"]}).reset_index()
    raised_by_type_grouop.columns = ["Tipo infraccion", "total"]
    fig = px.pie(raised_by_type_grouop, names="Tipo infraccion", values="total",
                 color_discrete_sequence=["#e6e6ff", "BlueViolet", "MidnightBlue", "Red"]
                 , category_orders={"Tipo infraccion": ["Fotomulta",
                                                        "Velocidad",
                                                        "PDA",
                                                        "Camara movil"]}
                 )
    fig.update_layout(
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
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(
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
    daily_payments_by_type_grouop = dataframe.groupby(["fecha_acreditacion", "Tipo infraccion"]).agg(
        {"total": ["sum"]}).reset_index()
    daily_payments_by_type_grouop.columns = ["Fecha pago", "Tipo infraccion", "total"]
    fig = px.bar(daily_payments_by_type_grouop, x="Fecha pago", y="total", color="Tipo infraccion",
                 color_discrete_sequence=["#e6e6ff", "BlueViolet", "MidnightBlue", "Red"], text_auto=True,
                 category_orders={"Tipo infraccion": ["Fotomulta",
                                                      "Velocidad",
                                                      "PDA",
                                                      "Camara movil"]})
    fig.update_layout(
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
        height=440,
    )
    fig.update_traces(textposition='inside', textfont_size=14)
    return fig
