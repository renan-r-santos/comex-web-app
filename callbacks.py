# Third party modules
import dash
from dash_table.Format import Format, Group, Scheme, Symbol
import pandas as pd
import plotly.graph_objects as go
import requests

# Current project modules
from app import app, API_ENDPOINT
import styles


# MONTH MAP
MONTH_MAP = pd.DataFrame(
    columns=["MES", "MONTH_LABEL"],
    data=list(
        zip(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            [
                "Jan",
                "Fev",
                "Mar",
                "Abr",
                "Mai",
                "Jun",
                "Jul",
                "Ago",
                "Set",
                "Out",
                "Nov",
                "Dez",
            ],
        )
    ),
)


@app.callback(
    [
        dash.dependencies.Output("geo-table", "data"),
        dash.dependencies.Output("geo-table", "columns"),
        dash.dependencies.Output("filter-year", "options"),
        dash.dependencies.Output("filter-type", "options"),
        dash.dependencies.Output("filter-product", "options"),
        dash.dependencies.Output("monthly-bar-chart", "figure"),
        dash.dependencies.Output("pie-chart", "figure"),
    ],
    [
        dash.dependencies.Input("filter-year", "value"),
        dash.dependencies.Input("filter-type", "value"),
        dash.dependencies.Input("filter-product", "value"),
        dash.dependencies.Input("filter-year", "options"),
        dash.dependencies.Input("filter-type", "options"),
        dash.dependencies.Input("filter-product", "options"),
    ],
)
def update_chart(
    year, mov_type, product, options_year, options_type, options_product
):

    if options_year is None or options_type is None or options_product is None:
        db_filter = requests.get(f"{API_ENDPOINT}/metadata").json()
        options_product = [{"label": "Todos", "value": "all"}] + db_filter[
            "sh2"
        ]
        options_type = [{"label": "Todos", "value": "all"}] + db_filter["type"]
        options_year = [{"label": "Todos", "value": "all"}] + db_filter["year"]

    # Initialize dict
    filters = {
        "year": year,
        "type": mov_type,
        "product": product,
    }

    # Check if select all is selected
    for f in filters.keys():
        if "all" in filters[f]:
            filters[f] = []

    # Use API to get data from the DB
    query_string = "&".join(
        [f"{key}={value}" for key, value in filters.items()]
    )
    query_string += f"&fields={[]}"
    data = requests.get(f"{API_ENDPOINT}/data?{query_string}")
    df = pd.read_json(data.text)

    # Prepare DataFrame
    table_df = df.groupby(by=["SG_UF"], as_index=False).agg({"VL_FOB": "sum"})
    table_df["CONTRIB"] = table_df["VL_FOB"] / table_df["VL_FOB"].sum()

    # Configure table data
    table_data = table_df.to_dict("records")
    table_columns = [
        {"id": "SG_UF", "name": "Estado"},
        {
            "id": "VL_FOB",
            "name": "Total",
            "type": "numeric",
            "format": Format(
                symbol=Symbol.yes,
                symbol_prefix="US$ ",
                group_delimiter=".",
                group=Group.yes,
                groups=[3],
            ),
        },
        {
            "id": "CONTRIB",
            "name": "Participação",
            "type": "numeric",
            "format": Format(
                precision=2, scheme=Scheme.percentage, decimal_delimiter=","
            ),
        },
    ]

    # Monthly total graph
    hovertemplate_xy = (
        "<i>Mês-Ano</i>: %{x}<br>" + "<i>Total</i>: %{y:,d}" + "<extra></extra>"
    )
    monthly_df = df.groupby(by=["ANO", "MES"], as_index=False).agg(
        {"VL_FOB": "sum"}
    )
    monthly_df = monthly_df.merge(MONTH_MAP, how="inner", on="MES")
    monthly_df["XAXIS_LABEL"] = (
        monthly_df["MONTH_LABEL"] + "-" + monthly_df["ANO"].astype(str).str[2:]
    )
    monthly_df.sort_values(["ANO", "MES"], inplace=True)
    monthly_df.reset_index(inplace=True, drop=True)

    monthly_data = go.Bar(
        x=monthly_df.index + 1,
        y=monthly_df["VL_FOB"],
        marker={"color": styles.colors["light-green"], "opacity": 0.75},
        hovertemplate=hovertemplate_xy,
    )

    monthly_fig = go.Figure(data=monthly_data, layout=styles.go_layout)
    monthly_fig.update_layout(
        title={"text": "Total mês a mês"},
        titlefont={"size": 22},
        xaxis={
            "title": "Mês-Ano",
            "tickvals": monthly_df.index + 1,
            "ticktext": monthly_df["XAXIS_LABEL"],
        },
        yaxis={"title": "Total (US$)"},
        showlegend=False,
    )

    # Via pie plot
    pie_df = df.groupby(by=["COD_VIA"], as_index=False).agg({"VL_FOB": "sum"})
    via_data = requests.get(f"{API_ENDPOINT}/via")
    via_labels_df = pd.read_json(via_data.text)
    pie_df = pie_df.merge(via_labels_df, how="inner", on="COD_VIA")
    hovertemplate_xy = (
        "<i>Via</i>: %{label}<br>"
        + "<i>Participação</i>: %{percent:.2%}<br>"
        + "<i>Total</i>: %{value:,d}"
        + "<extra></extra>"
    )
    pie_data = go.Pie(
        labels=pie_df["NO_VIA"],
        values=pie_df["VL_FOB"],
        hovertemplate=hovertemplate_xy,
    )
    pie_fig = go.Figure(data=pie_data, layout=styles.go_layout)
    pie_fig.update_traces(textposition="inside", texttemplate="%{percent:.2%f}")
    pie_fig.update_layout(
        title={"text": "Participação das vias"},
        titlefont={"size": 22},
        legend=dict(x=1, y=-0.4, font=dict(size=12)),
        uniformtext_mode="hide",
        uniformtext_minsize=20,
        height=600,
    )

    return (
        table_data,
        table_columns,
        options_year,
        options_type,
        options_product,
        monthly_fig,
        pie_fig,
    )
