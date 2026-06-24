from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["age", "bmi", "children"]),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["sex", "smoker", "region"]),
    ],
    remainder="drop"
)