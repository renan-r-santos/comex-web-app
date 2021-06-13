# Third party modules
import dash
import dash_core_components as dcc
import dash_html_components as html

# Current project modules
from app import app
from app import server
import callbacks
from layouts import layout

app.layout = layout


if __name__ == "__main__":
    app.run_server(debug=False)
