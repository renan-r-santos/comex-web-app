# Standard modules
from datetime import datetime

# Third party modules
import pandas as pd

BASE_URL = (
    "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/{}_{}.csv"
)
OUTPUT_DIR = "data"

# Get last 3 full years
years = [datetime.now().year - i for i in range(1, 4)]

# Set types of movement
mov_types = [
    {"label": "Exportação", "value": "EXP"},
    {"label": "Importação", "value": "IMP"},
]

# Download data
f_comex_df = pd.DataFrame()
for year in years:
    for mov_type in mov_types:
        temp_df = pd.read_csv(BASE_URL.format(mov_type["value"], year), sep=";")
        temp_df["MOVIMENTACAO"] = mov_type["label"]
        f_comex_df = f_comex_df.append(temp_df)

# Fix column names
f_comex_df.columns = [
    "ANO",
    "MES",
    "COD_NCM",
    "COD_UNIDADE",
    "COD_PAIS",
    "SG_UF",
    "COD_VIA",
    "COD_URF",
    "VL_QUANTIDADE",
    "VL_PESO_KG",
    "VL_FOB",
    "MOVIMENTACAO",
]

# Add leading zeros
# There is no column CO_SH4 in this database, so ignore this
# "Preencher com zero à esquerda as seguintes variáveis nas seguintes quantidades: COD_SH4=4"
f_comex_df["COD_NCM"] = f_comex_df["COD_NCM"].apply(
    lambda x: "{0:0>8}".format(x)
)
f_comex_df["COD_URF"] = f_comex_df["COD_URF"].apply(
    lambda x: "{0:0>7}".format(x)
)
f_comex_df["COD_PAIS"] = f_comex_df["COD_PAIS"].apply(
    lambda x: "{0:0>3}".format(x)
)

# Optionally save the data
# f_comex_df.to_csv(f"{OUTPUT_DIR}/f_comex.csv", index=False, sep=";")
