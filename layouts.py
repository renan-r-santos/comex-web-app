# Third party modules
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import requests

# Current project modules
from app import app, API_ENDPOINT
import styles


# Header with logo
def get_header():
    header = html.Div(
        [
            html.Div(
                [], className="col-2"
            ),  # Same as img width, allowing to have the title centrally aligned
            html.Div(
                [
                    html.H1(
                        children="Comex data viewer",
                        style={
                            "textAlign": "center",
                            "fontWeight": "bold",
                            "color": styles.colors["medium-blue-grey"],
                        },
                    )
                ],
                className="col-8",
                style={"padding-top": "1%", "padding-bottom": "1%"},
            ),
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("logo.png"),
                        height="65px",
                        width="auto",
                    )
                ],
                className="col-2",
                style={
                    "align-items": "center",
                    "padding-top": "1%",
                    "height": "auto",
                },
            ),
        ],
        className="row",
        style={
            "height": "4%",
            "background-color": styles.colors["light-green"],
        },
    )
    return header


# Returns an empty row of a defined height
def get_emptyrow(h="45px"):
    emptyrow = html.Div(
        [html.Div([html.Br()], className="col-12")],
        className="row",
        style={"height": h},
    )
    return emptyrow


layout = html.Div(
    [
        #####################
        # Row 1: Header
        get_header(),
        #####################
        # Row 2: Filters
        html.Div(
            [  # External row
                html.Div(
                    [  # External 12 columns
                        html.Div(
                            [  # Internal row
                                # 3 blank columns
                                html.Div(
                                    [], className="col-1"
                                ),  # Blank 2 columns
                                html.H5(
                                    children="Filtros:",
                                    style={
                                        "margin-top": "15px",
                                        "margin-bottom": "5px",
                                        "text-align": "right",
                                        "paddingLeft": 5,
                                        "color": styles.colors["white"],
                                    },
                                    className="col-1",
                                ),
                                # Year filter
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        dcc.Dropdown(
                                                            id="filter-year",
                                                            value=[],
                                                            multi=True,
                                                            placeholder="Ano",
                                                            style={
                                                                "font-size": (
                                                                    "13px"
                                                                ),
                                                                "color": styles.colors[
                                                                    "medium-blue-grey"
                                                                ],
                                                                "white-space": (
                                                                    "nowrap"
                                                                ),
                                                                "text-overflow": (
                                                                    "ellipsis"
                                                                ),
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "width": "70%",
                                                        "margin-top": "5px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "margin-top": "10px",
                                                "margin-bottom": "5px",
                                                "text-align": "left",
                                                "paddingLeft": 5,
                                            },
                                        )
                                    ],
                                    className="col-1",
                                ),  # Year filter
                                # Type filter
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        dcc.Dropdown(
                                                            id="filter-type",
                                                            value=[],
                                                            multi=True,
                                                            placeholder=(
                                                                "Tipo de"
                                                                " movimentação"
                                                            ),
                                                            style={
                                                                "font-size": (
                                                                    "13px"
                                                                ),
                                                                "color": styles.colors[
                                                                    "medium-blue-grey"
                                                                ],
                                                                "white-space": (
                                                                    "nowrap"
                                                                ),
                                                                "text-overflow": (
                                                                    "ellipsis"
                                                                ),
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "width": "70%",
                                                        "margin-top": "5px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "margin-top": "10px",
                                                "margin-bottom": "5px",
                                                "text-align": "left",
                                                "paddingLeft": 5,
                                            },
                                        )
                                    ],
                                    className="col-2",
                                ),  # Type filter
                                # Product filter
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        dcc.Dropdown(
                                                            id="filter-product",
                                                            value=[],
                                                            multi=True,
                                                            placeholder=(
                                                                "Tipo de"
                                                                " produto"
                                                            ),
                                                            style={
                                                                "font-size": (
                                                                    "13px"
                                                                ),
                                                                "color": styles.colors[
                                                                    "medium-blue-grey"
                                                                ],
                                                                "white-space": (
                                                                    "nowrap"
                                                                ),
                                                                "text-overflow": (
                                                                    "ellipsis"
                                                                ),
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "width": "70%",
                                                        "margin-top": "5px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "margin-top": "10px",
                                                "margin-bottom": "5px",
                                                "text-align": "left",
                                                "paddingLeft": 5,
                                            },
                                        )
                                    ],
                                    className="col-6",
                                ),  # Product filter
                                # 3 blank columns
                                html.Div(
                                    [], className="col-1"
                                ),  # Blank 2 columns
                            ],
                            className="row",
                            style={
                                "margin-top": "20px",
                                "margin-bottom": "20px",
                            },
                        )  # Internal row
                    ],
                    className="col-12",
                    style=styles.filterdiv_borderstyling,
                )  # External 12 columns
            ],
            className="row sticky-top",
        ),  # External row
        ####################
        # Row 3
        get_emptyrow(),
        #####################
        # Row 4: Charts
        html.Div(
            [  # External row
                html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Painel Comex",
                            style={
                                "color": styles.colors["white"],
                                "margin-top": "10px",
                                "margin-bottom": "30px",
                            },
                        ),
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                html.Div(
                                    [dcc.Graph(id="monthly-bar-chart")],
                                    className="col-5",
                                ),
                                # Chart Column
                                html.Div(
                                    [dcc.Graph(id="pie-chart")],
                                    className="col-5",
                                ),
                                # Table ColumN
                                html.Div(
                                    [
                                        dash_table.DataTable(
                                            id="geo-table",
                                            sort_action="native",
                                            style_header={
                                                "backgroundColor": (
                                                    "transparent"
                                                ),
                                                "fontFamily": styles.font_family,
                                                "font-size": "1rem",
                                                "color": styles.colors[
                                                    "light-green"
                                                ],
                                                "border": "0px transparent",
                                                "textAlign": "center",
                                            },
                                            style_cell={
                                                "backgroundColor": (
                                                    "transparent"
                                                ),
                                                "fontFamily": styles.font_family,
                                                "font-size": "0.85rem",
                                                "color": styles.colors["white"],
                                                "border": "0px transparent",
                                                "textAlign": "center",
                                            },
                                            cell_selectable=False,
                                            column_selectable=False,
                                        )
                                    ],
                                    className="col-2",
                                ),
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-10",
                    style=styles.externalgraph_colstyling,
                ),  # External 10-column
                html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=styles.externalgraph_rowstyling,
        ),
    ]  # External row
)
