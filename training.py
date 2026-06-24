import mlflow
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from config import DATABASE_URL
from preprocessing import preprocessor

mlflow.set_tracking_uri("http://localhost:5000")

engine = create_engine(DATABASE_URL)
df = pd.read_sql_table(table_name="dataset", con=engine)

X = df.drop(columns=["charges"])
y = df["charges"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

mlflow.set_experiment("insurance-prediction")

def log_model(model, model_name):
    with mlflow.start_run(run_name=model_name):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)

        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(model, model_name)
        print(f"{model_name}. MSE: {mse}, RMSE: {rmse}, MAE: {mae}")

linear_model = LinearRegression()
log_model(linear_model, "Linear Regression")

tree_model = DecisionTreeRegressor()
log_model(tree_model, "Decision Tree Regressor")

forest_model = RandomForestRegressor()
log_model(forest_model, "Random Forest Regressor")

print("Experiment completed! Check the MLflow server for details.")