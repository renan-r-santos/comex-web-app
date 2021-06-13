# Standard modules
import ast
import json
import os

# Third party modules
import dash
import flask
import pymongo

# Securely get MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = pymongo.MongoClient(MONGODB_URI)

# Declare the database
db = client.comex_db

app = dash.Dash(__name__)
server = app.server


@server.route("/api/data")
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
    data = list(cursor)
    return json.dumps(data)
