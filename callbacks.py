# Third party modules
import dash
from dash_table.Format import Format, Group, Scheme, Symbol
import pandas as pd
import requests

# Current project modules
from app import app

API_ENDPOINT = "http://127.0.0.1:8050/api"


@app.callback(
    [
        dash.dependencies.Output("geo-table", "data"),
        dash.dependencies.Output("geo-table", "columns"),
    ],
    [
        dash.dependencies.Input("filter-year", "value"),
        dash.dependencies.Input("filter-type", "value"),
        dash.dependencies.Input("filter-product", "value"),
    ],
)
def update_chart(year, mov_type, product):

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
    query_string += f"&fields={['SG_UF', 'VL_FOB']}"
    data = requests.get(f"{API_ENDPOINT}/data?{query_string}")
    df = pd.read_json(data.text)

    # Prepare DataFrame
    df = df.groupby(by=["SG_UF"], as_index=False).agg({"VL_FOB": "sum"})
    df["CONTRIB"] = df["VL_FOB"] / df["VL_FOB"].sum()

    # Configure table data
    data = df.to_dict("records")
    columns = [
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

    return data, columns
