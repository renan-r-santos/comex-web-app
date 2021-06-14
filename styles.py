# Third party modules
import plotly.graph_objects as go

# Styling
colors = {
    "dark-blue-grey": "rgb(62, 64, 76)",
    "medium-blue-grey": "rgb(77, 79, 91)",
    "superdark-green": "rgb(41, 56, 55)",
    "dark-green": "rgb(57, 81, 85)",
    "medium-green": "rgb(93, 113, 120)",
    "light-green": "rgb(186, 218, 212)",
    "pink-red": "rgb(255, 101, 131)",
    "dark-pink-red": "rgb(247, 80, 99)",
    "white": "rgb(251, 251, 252)",
    "light-grey": "rgb(208, 206, 206)",
}

filterdiv_borderstyling = {
    "border-radius": "0px 0px 10px 10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": colors["light-green"],
    "background-color": colors["superdark-green"],
}

font_family = "Circular Std"

externalgraph_rowstyling = {"margin-left": "15px", "margin-right": "15px"}

externalgraph_colstyling = {
    "border-radius": "10px",
    "border-style": "solid",
    "border-width": "1px",
    "border-color": colors["superdark-green"],
    "background-color": colors["superdark-green"],
    "box-shadow": "0px 0px 17px 0px rgba(186, 218, 212, .5)",
    "padding-top": "10px",
    "padding-bottom": "30px",
}

go_title = {"font": {"size": 16, "color": colors["white"]}}

go_xaxis = {
    "showgrid": False,
    "linecolor": colors["light-grey"],
    "color": colors["light-grey"],
    "tickangle": 315,
    "titlefont": {"size": 12, "color": colors["light-grey"]},
    "tickfont": {"size": 11, "color": colors["light-grey"]},
    "zeroline": False,
}

go_yaxis = {
    "showgrid": True,
    "color": colors["light-grey"],
    "gridwidth": 0.5,
    "gridcolor": colors["dark-green"],
    "linecolor": colors["light-grey"],
    "titlefont": {"size": 12, "color": colors["light-grey"]},
    "tickfont": {"size": 11, "color": colors["light-grey"]},
    "zeroline": False,
}

go_legend = {
    "orientation": "h",
    "yanchor": "bottom",
    "y": 1.01,
    "xanchor": "right",
    "x": 1.05,
    "font": {"size": 9, "color": colors["light-grey"]},
}  # Legend will be on the top right, above the graph, horizontally

go_margins = {
    "l": 5,
    "r": 5,
    "t": 45,
    "b": 15,
}  # Set top margin to in case there is a legend

go_layout = go.Layout(
    font={"family": font_family},
    title=go_title,
    title_x=0.5,  # Align chart title to center
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=go_xaxis,
    yaxis=go_yaxis,
    height=800,
    legend=go_legend,
    margin=go_margins,
    separators=",.",
)
