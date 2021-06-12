# Third party modules
import numpy as np
import pandas as pd
import pymongo

# Add _id column for MongoDB indexing
def add_mongodb_id(df):
    df["_id"] = list(range(1, len(df) + 1))


# Main function
def main():
    # Read data
    d_via_df = pd.read_excel("data/d_via.xlsx")
    d_sh2_df = pd.read_excel("data/d_sh2.xlsx")
    f_comex_df = pd.read_csv("data/f_comex.csv", sep=";")
    uf_data_df = pd.read_csv("data/uf_data.csv", sep=";", index_col=1)

    # Rename sh2 column names to match names of f_comex DataFrame
    d_sh2_df.rename(columns={"CO_NCM": "COD_NCM"}, inplace=True)
    d_sh2_df.rename(columns={"CO_SH2": "COD_SH2"}, inplace=True)

    # Cap data to 4M rows by randomly deleting rows
    # We need this temporary because of MongoDB Atlas free tier size limit
    drop_indices = np.random.choice(
        f_comex_df.index, len(f_comex_df) - 4000000, replace=False
    )
    f_comex_df.drop(drop_indices, inplace=True)
    f_comex_df.reset_index(drop=True, inplace=True)

    # Map SH4 code to SH2
    f_comex_df["COD_SH2"] = f_comex_df["COD_NCM"].map(
        d_sh2_df.set_index("COD_NCM").to_dict()["COD_SH2"]
    )

    # Map SG_UF string do COD_UF
    # There 4 codes that are not Brazilian states:
    # 'ND', 'EX', 'ZN', 'RE'
    # Rows with these codes will be dropped later using dropna
    f_comex_df["COD_UF"] = f_comex_df["SG_UF"].map(
        uf_data_df.to_dict()["COD_UF"]
    )

    # Convert column MOVIMENTACAO to boolean
    f_comex_df["MOVIMENTACAO"].replace(
        {"Exportação": 1, "Importação": 0}, inplace=True
    )

    # Drop columns not used in order to decrease the size of the db
    f_comex_df.drop(
        columns=[
            "COD_NCM",
            "COD_UNIDADE",
            "COD_PAIS",
            "SG_UF",
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

    # Drop rows with na values (non Brazilian UF codes - see above)
    f_comex_df.dropna(inplace=True)
    f_comex_df.reset_index(drop=True, inplace=True)

    # Drop sh2 duplicates
    d_sh2_df.drop_duplicates(inplace=True)
    d_sh2_df.reset_index(drop=True, inplace=True)

    # Convert DataFrame to int32
    f_comex_df = f_comex_df.astype(int)

    # Add _id column for MongoDB indexing
    add_mongodb_id(d_via_df)
    add_mongodb_id(d_sh2_df)
    add_mongodb_id(f_comex_df)
    add_mongodb_id(uf_data_df)

    # Connect to db
    conn = (
        "mongodb://admin:***REMOVED***@comexcluster0-shard-00-00.ufiic.mongodb.net:27017,"
        "comexcluster0-shard-00-01.ufiic.mongodb.net:27017,"
        "comexcluster0-shard-00-02.ufiic.mongodb.net:27017/?"
        "ssl=true&replicaSet=atlas-7gjvee-shard-0&authSource=admin&retryWrites=true&w=majority"
    )
    client = pymongo.MongoClient(conn)

    # Declare the database
    db = client.comex_db

    # Drop collection to reset database
    db.d_via.drop()
    db.d_sh2.drop()
    db.f_comex.drop()
    db.uf_data.drop()

    # Convert pandas dataframe to dictionary and insert into MongoDB
    db.d_via.insert_many(d_via_df.to_dict(orient="records"))
    db.d_sh2.insert_many(d_sh2_df.to_dict(orient="records"))
    db.f_comex.insert_many(f_comex_df.to_dict(orient="records"))
    db.uf_data.insert_many(uf_data_df.to_dict(orient="records"))

    print("MongoDB successfully created")


if __name__ == "__main__":
    main()
