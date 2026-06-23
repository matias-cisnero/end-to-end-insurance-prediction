import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URL, DATASET_URL

df = pd.read_csv(DATASET_URL)
engine = create_engine(DATABASE_URL)

df.to_sql(name="dataset", con=engine, if_exists="replace", index=False)