import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URI, DATASET_URI

df = pd.read_csv(DATASET_URI)
engine = create_engine(DATABASE_URI)

df.to_sql(name="dataset", con=engine, if_exists="replace", index=False)