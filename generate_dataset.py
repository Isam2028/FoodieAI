
import pandas as pd
import numpy as np
from pathlib import Path

# Make results reproducible
np.random.seed(42)

# Number of delivery records
number_of_records = 1000

# Generate delivery information
data = {
    "distance_km": np.random.uniform(1, 15, number_of_records),

    "traffic_level": np.random.choice(
        ["Low", "Medium", "High"],
        number_of_records
    ),

    "weather": np.random.choice(
        ["Clear", "Cloudy", "Rainy"],
        number_of_records
    ),

    "preparation_time_min": np.random.randint(
        5, 31, number_of_records
    ),

    "courier_experience_years": np.random.uniform(
        0, 10, number_of_records
    ),

    "time_of_day": np.random.choice(
        ["Morning", "Afternoon", "Evening", "Night"],
        number_of_records
    )
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Calculate additional time based on traffic
traffic_delay = df["traffic_level"].map({
    "Low": 2,
    "Medium": 7,
    "High": 15
})

# Calculate additional time based on weather
weather_delay = df["weather"].map({
    "Clear": 0,
    "Cloudy": 3,
    "Rainy": 8
})

# Additional time based on time of day
time_delay = df["time_of_day"].map({
    "Morning": 1,
    "Afternoon": 3,
    "Evening": 7,
    "Night": 2
})

# Generate delivery time
df["delivery_time_min"] = (
    df["preparation_time_min"]
    + df["distance_km"] * 3
    + traffic_delay
    + weather_delay
    + time_delay
    - df["courier_experience_years"] * 0.5
    + np.random.normal(0, 2, number_of_records)
)

# Ensure delivery time is positive
df["delivery_time_min"] = df["delivery_time_min"].clip(lower=5)

# Round numerical values
df["distance_km"] = df["distance_km"].round(2)
df["courier_experience_years"] = df[
    "courier_experience_years"
].round(1)

df["delivery_time_min"] = df[
    "delivery_time_min"
].round(2)

# Create dataset folder if necessary
Path("dataset").mkdir(exist_ok=True)

# Save dataset as CSV
df.to_csv("dataset/delivery_data.csv", index=False)

print("Dataset generated successfully!")
print("Total records:", len(df))

print("\nFirst 5 delivery records:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nDataset saved at dataset/delivery_data.csv")
