
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("dataset/delivery_data.csv")

# Separate features and target
X = df.drop("delivery_time_min", axis=1)
y = df["delivery_time_min"]

# Categorical columns
categorical_columns = [
    "traffic_level",
    "weather",
    "time_of_day"
]

# Preprocessing
def create_preprocessor():
    return ColumnTransformer(
        transformers=[
            ("categorical",
             OneHotEncoder(handle_unknown="ignore"),
             categorical_columns)
        ],
        remainder="passthrough"
    )

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define algorithms
models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
}

results = []
trained_models = {}

# Train and evaluate both models
for name, algorithm in models.items():

    model = Pipeline(steps=[
        ("preprocessor", create_preprocessor()),
        ("regressor", algorithm)
    ])

    print("\nTraining:", name)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    results.append({
        "Model": name,
        "MAE": round(mae, 3),
        "RMSE": round(rmse, 3),
        "R2 Score": round(r2, 4)
    })

    trained_models[name] = model

    print("MAE:", round(mae, 3))
    print("RMSE:", round(rmse, 3))
    print("R2 Score:", round(r2, 4))

# Compare models
results_df = pd.DataFrame(results)

print("\nMODEL COMPARISON")
print(results_df.to_string(index=False))

# Select model with lowest MAE
best_model_name = results_df.loc[
    results_df["MAE"].idxmin(), "Model"
]

best_model = trained_models[best_model_name]

# Save models
Path("models").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)

joblib.dump(
    trained_models["Linear Regression"],
    "models/linear_regression.pkl"
)

joblib.dump(
    trained_models["Random Forest"],
    "models/random_forest.pkl"
)

joblib.dump(
    best_model,
    "models/delivery_model.pkl"
)

results_df.to_json(
    "outputs/model_metrics.json",
    orient="records",
    indent=4
)

print("\nBEST MODEL:", best_model_name)
print("Best model saved successfully!")
