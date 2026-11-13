
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("dataset/delivery_data.csv")

# Graph 1: Distance vs Delivery Time
plt.figure(figsize=(8, 5))
plt.scatter(df["distance_km"], df["delivery_time_min"])
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Time (minutes)")
plt.title("Distance vs Delivery Time")
plt.grid()
plt.show()

# Graph 2: Traffic vs Delivery Time
traffic_avg = df.groupby("traffic_level")[
    "delivery_time_min"
].mean()

plt.figure(figsize=(8, 5))
traffic_avg.plot(kind="bar")
plt.xlabel("Traffic Level")
plt.ylabel("Average Delivery Time (minutes)")
plt.title("Traffic Level vs Delivery Time")
plt.xticks(rotation=0)
plt.grid(axis="y")
plt.show()

# Graph 3: Weather vs Delivery Time
weather_avg = df.groupby("weather")[
    "delivery_time_min"
].mean()

plt.figure(figsize=(8, 5))
weather_avg.plot(kind="bar")
plt.xlabel("Weather")
plt.ylabel("Average Delivery Time (minutes)")
plt.title("Weather vs Delivery Time")
plt.xticks(rotation=0)
plt.grid(axis="y")
plt.show()

print("Data visualization completed!")
