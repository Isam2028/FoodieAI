
import sqlite3

# Database file location
DATABASE_PATH = "foodieai.db"


# Connect to database
def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    return connection


# Create prediction history table
def create_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            distance_km REAL NOT NULL,

            traffic_level TEXT NOT NULL,

            weather TEXT NOT NULL,

            preparation_time_min REAL NOT NULL,

            courier_experience_years REAL NOT NULL,

            time_of_day TEXT NOT NULL,

            predicted_time REAL NOT NULL,

            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


# Save a prediction
def save_prediction(
    distance,
    traffic,
    weather,
    preparation,
    experience,
    time_of_day,
    predicted_time
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO prediction_history (
            distance_km,
            traffic_level,
            weather,
            preparation_time_min,
            courier_experience_years,
            time_of_day,
            predicted_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        distance,
        traffic,
        weather,
        preparation,
        experience,
        time_of_day,
        predicted_time
    ))

    connection.commit()

    connection.close()

# Initialize database
if __name__ == "__main__":

    create_table()

    print("FoodieAI database created successfully!")

    print("Prediction history table is ready!")