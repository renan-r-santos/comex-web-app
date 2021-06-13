# Standard modules
import os

# Third party modules
import numpy as np
import pandas as pd
import pymongo

# Securely get MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

# Add _id column for MongoDB indexing
def add_mongodb_id(df):
    df["_id"] = list(range(1, len(df) + 1))


# Main function
def main():
    # Read data
    d_via_df = pd.read_excel("data/d_via.xlsx")
    d_sh2_df = pd.read_excel("data/d_sh2.xlsx")
    f_comex_df = pd.read_csv("data/f_comex.csv", sep=";")

    # Rename sh2 column names to match the names used in f_comex DataFrame
    d_sh2_df.rename(columns={"CO_NCM": "COD_NCM"}, inplace=True)
    d_sh2_df.rename(columns={"CO_SH2": "COD_SH2"}, inplace=True)

    # Map SH4 code to SH2 code, since SH4 is not used in this MVP
    f_comex_df = f_comex_df.merge(
        d_sh2_df[["COD_NCM", "COD_SH2"]], how="inner", on="COD_NCM"
    )

    # Convert column MOVIMENTACAO to boolean
    f_comex_df["MOVIMENTACAO"].replace(
        {"Exportação": 1, "Importação": 0}, inplace=True
    )

    # Drop columns not used in the MVP to decrease the size of the db
    f_comex_df.drop(
        columns=[
            "COD_NCM",
            "COD_UNIDADE",
            "COD_PAIS",
            "COD_URF",
            "VL_QUANTIDADE",
            "VL_PESO_KG",
        ],
        inplace=True,
    )
    d_sh2_df.drop(
        columns=[
            "COD_NCM",
            "NO_NCM_POR",
        ],
        inplace=True,
    )

    # Drop sh2 duplicates
    d_sh2_df.drop_duplicates(inplace=True)
    d_sh2_df.reset_index(drop=True, inplace=True)

    # Aggregate and sum total FOB value of rows that have the same product,
    # year, month, via, uf and type to drastically optimize and reduce db size
    f_comex_df = f_comex_df.groupby(
        by=["ANO", "MES", "COD_VIA", "MOVIMENTACAO", "SG_UF", "COD_SH2"],
        as_index=False,
    ).agg({"VL_FOB": "sum"})

    # There 4 codes that are not Brazilian states:
    # 'ND', 'EX', 'ZN', 'RE'
    # Drop those
    f_comex_df = f_comex_df[~f_comex_df["SG_UF"].isin(["ND", "EX", "ZN", "RE"])]

    # Add _id column for MongoDB indexing
    add_mongodb_id(d_via_df)
    add_mongodb_id(d_sh2_df)
    add_mongodb_id(f_comex_df)

    # Connect to db
    client = pymongo.MongoClient(MONGODB_URI)

    # Declare the database
    db = client.comex_db

    # Drop collection to reset database
    db.d_via.drop()
    db.d_sh2.drop()
    db.f_comex.drop()

    # Convert pandas dataframe to dictionary and insert into MongoDB
    db.d_via.insert_many(d_via_df.to_dict(orient="records"))
    db.d_sh2.insert_many(d_sh2_df.to_dict(orient="records"))
    db.f_comex.insert_many(f_comex_df.to_dict(orient="records"))

    # After all optimizations, MongoDB Atlas size is:
    # DATABASE SIZE: 2.66MB
    # INDEX SIZE: 860KB
    # TOTAL COLLECTIONS: 3
    print("MongoDB successfully created")


if __name__ == "__main__":
    main()
