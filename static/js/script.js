
// =====================================
// 1. SELECT HTML ELEMENTS
// =====================================

const predictionForm = document.getElementById("predictionForm");

const predictButton = document.getElementById("predictButton");

const resultTime = document.getElementById("resultTime");

const resultMessage = document.getElementById("resultMessage");

const errorMessage = document.getElementById("errorMessage");


// =====================================
// 2. HANDLE FORM SUBMISSION
// =====================================

predictionForm.addEventListener("submit", async function(event) {

    // Prevent page refresh
    event.preventDefault();

    // Clear previous errors
    errorMessage.style.display = "none";
    errorMessage.textContent = "";

    // Get input values
    const distance = Number(document.getElementById("distance").value);

    const traffic = document.getElementById("traffic").value;

    const weather = document.getElementById("weather").value;

    const preparation = Number(document.getElementById("preparation").value);

    const experience = Number(document.getElementById("experience").value);

    const timeOfDay = document.getElementById("time").value;


    // =====================================
    // 3. VALIDATE INPUTS
    // =====================================

    if (
        !Number.isFinite(distance) ||
        !Number.isFinite(preparation) ||
        !Number.isFinite(experience) ||
        distance < 0.1 || distance > 15 ||
        preparation < 5 || preparation > 30 ||
        experience < 0 || experience > 10
    ) {

        errorMessage.textContent =
            "Please enter valid values within the allowed ranges.";

        errorMessage.style.display = "block";

        return;
    }


    // =====================================
    // 4. PREPARE DATA FOR FLASK
    // =====================================

    const deliveryData = {

        distance_km: distance,

        traffic_level: traffic,

        weather: weather,

        preparation_time_min: preparation,

        courier_experience_years: experience,

        time_of_day: timeOfDay

    };


    // =====================================
    // 5. SEND DATA TO PYTHON BACKEND
    // =====================================

    predictButton.disabled = true;

    predictButton.innerHTML = "Predicting...";

    resultTime.innerHTML = "-- <span>min</span>";

    resultMessage.textContent =
        "Our Machine Learning model is processing your order...";

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(deliveryData)

        });


        const result = await response.json();


        if (!response.ok) {

            throw new Error(
                result.error || "Prediction failed."
            );

        }


        // =====================================
        // 6. DISPLAY PREDICTION
        // =====================================

        const predictedTime = Number(result.predicted_time);

        if (!Number.isFinite(predictedTime)) {
            throw new Error("Invalid prediction received.");
        }

        resultTime.innerHTML =
            `${predictedTime.toFixed(2)} <span>min</span>`;

        resultMessage.textContent =
            "Your delivery time has been estimated successfully!";

        resultMessage.style.color = "#34D399";


        // Scroll to result on smaller screens
        document.querySelector(".result-panel").scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    } catch (error) {

        // =====================================
        // 7. HANDLE ERRORS
        // =====================================

        errorMessage.textContent =
            error.message || "Unable to connect to the server.";

        errorMessage.style.display = "block";

        resultMessage.textContent =
            "Please try again.";

        resultMessage.style.color = "#FCA5A5";

    } finally {

        // Enable button again
        predictButton.disabled = false;

        predictButton.innerHTML =
            '<i data-lucide="sparkles"></i> Predict Delivery Time';

        if (window.lucide) {
            lucide.createIcons();
        }

    }

});


// =====================================
// 8. PAGE INITIALIZATION
// =====================================

console.log("FoodieAI JavaScript loaded successfully!");
