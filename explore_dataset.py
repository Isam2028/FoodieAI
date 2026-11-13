
import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/delivery_data.csv")

# 1. Display first 5 records
print("\nFIRST 5 RECORDS")
print(df.head())

# 2. Display dataset shape
print("\nDATASET SHAPE")
print("Rows and Columns:", df.shape)

# 3. Display column names
print("\nCOLUMN NAMES")
print(df.columns.tolist())

# 4. Display dataset information
print("\nDATASET INFORMATION")
df.info()

# 5. Display statistical summary
print("\nSTATISTICAL SUMMARY")
print(df.describe())

# 6. Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# 7. Check duplicate records
print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

print("\nDATASET EXPLORATION COMPLETED!")
