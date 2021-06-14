# Standard modules
import ast
import json
import os

# Third party modules
import dash
import flask
import pandas as pd
import pymongo

# API ENDPOINT
API_ENDPOINT = "https://comex-web-app.herokuapp.com/api"

# Securely get MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = pymongo.MongoClient(MONGODB_URI)

# Declare the database
db = client.comex_db

app = dash.Dash(__name__)
server = app.server


# Convert a cursor result to a ready-to-use dropdown options
def dict2dropdown(cursor):
    df = pd.DataFrame(list(cursor))
    df.columns = ["value", "label"]
    df = df[["label", "value"]]
    return df.to_dict("records")


@server.route("/api/data", methods=["GET"])
def data():
    # Get filters
    year = flask.request.args.get("year")
    mov_type = flask.request.args.get("type")
    product = flask.request.args.get("product")
    fields = flask.request.args.get("fields")

    # Convert string representation of list to list
    year = ast.literal_eval(year)
    mov_type = ast.literal_eval(mov_type)
    product = ast.literal_eval(product)
    fields = ast.literal_eval(fields)

    # Create query
    query = {}
    if year != []:
        query["ANO"] = {"$in": year}
    if mov_type != []:
        query["MOVIMENTACAO"] = {"$in": mov_type}
    if product != []:
        query["COD_SH2"] = {"$in": product}

    # Create fields dict
    query_fields = {"_id": 0}
    if fields != [""]:
        for f in fields:
            query_fields[f] = 1

    # Query the f_comex collection
    cursor = db.f_comex.find(query, query_fields)
    return json.dumps(list(cursor))


@server.route("/api/metadata", methods=["GET"])
def metadata():
    output = {}

    output["sh2"] = dict2dropdown(db.d_sh2.find({}, {"_id": 0}))

    output["year"] = [
        {"label": str(year), "value": year}
        for year in db.f_comex.distinct("ANO")
    ]

    # hardcoded for now
    output["type"] = [
        {"label": "Exportação", "value": 1},
        {"label": "Importação", "value": 0},
    ]

    return output


@server.route("/api/via", methods=["GET"])
def via():
    cursor = db.d_via.find({}, {"_id": 0})
    return json.dumps(list(cursor))
