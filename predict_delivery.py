
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("models/delivery_model.pkl")

print("FOOD DELIVERY TIME PREDICTION")
print("--------------------------------")

# Get input from user
distance = float(input("Enter delivery distance (km): "))
traffic = input("Enter traffic (Low/Medium/High): ").title()
weather = input("Enter weather (Clear/Cloudy/Rainy): ").title()
preparation = int(input("Enter preparation time (minutes): "))
experience = float(input("Enter courier experience (years): "))
time_of_day = input(
    "Enter time (Morning/Afternoon/Evening/Night): "
).title()

# Prepare input data
new_order = pd.DataFrame([{
    "distance_km": distance,
    "traffic_level": traffic,
    "weather": weather,
    "preparation_time_min": preparation,
    "courier_experience_years": experience,
    "time_of_day": time_of_day
}])

# Predict delivery time
prediction = model.predict(new_order)

# Display result
print("\n--------------------------------")
print("PREDICTED DELIVERY TIME")
print("--------------------------------")
print(f"Estimated time: {prediction[0]:.2f} minutes")
print("--------------------------------")
