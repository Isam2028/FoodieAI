
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import pandas as pd
import joblib
import json
from pathlib import Path
import math

from database import create_table, save_prediction, get_connection


# =====================================
# INITIALIZE FLASK APPLICATION
# =====================================

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "delivery_model.pkl"
DATASET_PATH = BASE_DIR / "dataset" / "delivery_data.csv"
METRICS_PATH = BASE_DIR / "outputs" / "model_metrics.json"


# =====================================
# LOAD TRAINED ML MODEL
# =====================================

if not MODEL_PATH.exists():
    raise FileNotFoundError("Trained ML model not found!")

model = joblib.load(MODEL_PATH)

# Initialize prediction history database
create_table()


# =====================================
# HOME PAGE
# =====================================

@app.route("/")
def home():
    return render_template("index.html")


# =====================================
# PREDICTION API
# =====================================

@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Receive JSON data
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No input data received."
            }), 400

        # Extract values
        distance = float(data["distance_km"])
        traffic = data["traffic_level"]
        weather = data["weather"]
        preparation = float(data["preparation_time_min"])
        experience = float(data["courier_experience_years"])
        time_of_day = data["time_of_day"]

        # Check numerical values
        if not all(map(math.isfinite, [
            distance, preparation, experience
        ])):
            return jsonify({
                "error": "Input values must be valid numbers."
            }), 400

        # Validate distance
        if not 0.1 <= distance <= 15:
            return jsonify({
                "error": "Distance must be between 0.1 and 15 km."
            }), 400

        # Validate preparation time
        if not 5 <= preparation <= 30:
            return jsonify({
                "error": "Preparation time must be between 5 and 30 minutes."
            }), 400

        # Validate courier experience
        if not 0 <= experience <= 10:
            return jsonify({
                "error": "Courier experience must be between 0 and 10 years."
            }), 400

        # Validate categorical values
        if traffic not in ["Low", "Medium", "High"]:
            return jsonify({
                "error": "Invalid traffic level."
            }), 400

        if weather not in ["Clear", "Cloudy", "Rainy"]:
            return jsonify({
                "error": "Invalid weather condition."
            }), 400

        if time_of_day not in [
            "Morning", "Afternoon", "Evening", "Night"
        ]:
            return jsonify({
                "error": "Invalid time of day."
            }), 400

        # Prepare input for ML model
        input_data = pd.DataFrame([{
            "distance_km": distance,
            "traffic_level": traffic,
            "weather": weather,
            "preparation_time_min": preparation,
            "courier_experience_years": experience,
            "time_of_day": time_of_day
        }])

        # Generate prediction
        prediction = float(model.predict(input_data)[0])

        # Save prediction to SQLite database
        save_prediction(
            distance,
            traffic,
            weather,
            preparation,
            experience,
            time_of_day,
            round(prediction, 2)
        )

        # Return prediction to JavaScript
        return jsonify({
            "success": True,
            "predicted_time": round(prediction, 2),
            "unit": "minutes",
            "model": "Linear Regression"
        })

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Please provide valid delivery information."
        }), 400

    except Exception:
        app.logger.exception("Prediction failed")

        return jsonify({
            "error": "Unable to generate prediction."
        }), 500


# =====================================
# ANALYTICS DASHBOARD
# =====================================

@app.route("/analytics")
def analytics():

    try:
        # Load dataset
        df = pd.read_csv(DATASET_PATH)

        # Load model comparison results
        with open(METRICS_PATH, "r") as file:
            metrics = json.load(file)

        # Calculate dataset statistics
        statistics = {
            "total_records": int(len(df)),

            "average_time": round(
                float(df["delivery_time_min"].mean()), 2
            ),

            "minimum_time": round(
                float(df["delivery_time_min"].min()), 2
            ),

            "maximum_time": round(
                float(df["delivery_time_min"].max()), 2
            )
        }

        # Traffic analysis
        traffic_stats = (
            df.groupby("traffic_level")["delivery_time_min"]
            .mean()
            .round(2)
            .to_dict()
        )

        # Weather analysis
        weather_stats = (
            df.groupby("weather")["delivery_time_min"]
            .mean()
            .round(2)
            .to_dict()
        )

        # Distance vs delivery time data
        distance_stats = {
            "distance": df["distance_km"].tolist(),
            "delivery_time": df["delivery_time_min"].tolist()
        }

        # Render analytics page
        return render_template(
            "analytics.html",
            statistics=statistics,
            metrics=metrics,
            traffic_stats=traffic_stats,
            weather_stats=weather_stats,
            distance_stats=distance_stats
        )

    except Exception:
        app.logger.exception("Analytics dashboard failed")

        return (
            "Unable to load analytics dashboard. "
            "Please check your dataset and model metrics files.",
            500
        )


# =====================================
# PREDICTION HISTORY PAGE
# =====================================

@app.route("/history")
def history():

    connection = None

    try:
        # Connect to SQLite database
        connection = get_connection()

        # Retrieve saved predictions
        df = pd.read_sql_query(
            "SELECT * FROM prediction_history ORDER BY id DESC",
            connection
        )

        # Convert database records into dictionaries
        predictions = df.to_dict(orient="records")

        # Display history page
        return render_template(
            "history.html",
            predictions=predictions,
            total_predictions=len(predictions)
        )

    except Exception:
        app.logger.exception("Prediction history page failed")

        return (
            "Unable to load prediction history. "
            "Please check your database and history.html file.",
            500
        )

    finally:
        if connection is not None:
            connection.close()

# =====================================
# EXPORT PREDICTION HISTORY TO CSV
# =====================================

@app.route("/export-history")
def export_history():

    connection = None

    try:
        connection = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM prediction_history ORDER BY id DESC",
            connection
        )

        csv_data = df.to_csv(index=False)

        output = BytesIO(csv_data.encode("utf-8"))

        return send_file(
            output,
            mimetype="text/csv",
            as_attachment=True,
            download_name="FoodieAI_Prediction_History.csv"
        )

    except Exception:
        app.logger.exception("CSV export failed")
        return "Unable to export prediction history.", 500

    finally:
        if connection is not None:
            connection.close()
# =====================================
# RUN FLASK SERVER
# =====================================

if __name__ == "__main__":
    app.run(
    debug=True,
    port=5001,
    use_reloader=False
)
