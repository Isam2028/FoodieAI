
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# 1. Load dataset
df = pd.read_csv("dataset/delivery_data.csv")

print("Dataset loaded successfully!")
print("Total records:", len(df))

# 2. Separate features and target
X = df.drop("delivery_time_min", axis=1)
y = df["delivery_time_min"]

# 3. Identify categorical columns
categorical_columns = [
    "traffic_level",
    "weather",
    "time_of_day"
]

# 4. Convert categorical values into numerical format
preprocessor = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(handle_unknown="ignore"),
         categorical_columns)
    ],
    remainder="passthrough"
)

# 5. Create the ML model
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# 6. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# 7. Train the model
print("\nTraining Machine Learning model...")
model.fit(X_train, y_train)

print("Model training completed!")

# 8. Make predictions
predictions = model.predict(X_test)

# 9. Evaluate the model
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANCE")
print("-------------------------")
print("MAE:", round(mae, 3), "minutes")
print("RMSE:", round(rmse, 3), "minutes")
print("R2 Score:", round(r2, 4))

# 10. Save the trained model
Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/delivery_model.pkl")

print("\nTrained model saved successfully!")

# 11. Display actual vs predicted values
results = pd.DataFrame({
    "Actual Time": y_test.values[:10],
    "Predicted Time": predictions[:10].round(2)
})

print("\nACTUAL VS PREDICTED DELIVERY TIME")
print(results)
