from flask import Flask, request, jsonify
import joblib
import numpy as np

# Initialize Flask App
app = Flask(__name__)

# Load the trained model
model = joblib.load("D://Projects and hackathons//Credit Card Fraud Detection//fraud_detection_model.pkl")

# ✅ Ensure this route accepts POST requests
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Ensure the 'features' key exists in the request
        if "features" not in data:
            return jsonify({"error": "Missing 'features' key in request"}), 400
        
        # Convert data to NumPy array
        features = np.array(data["features"]).reshape(1, -1)  # Ensure it’s 2D

        # Make prediction
        prediction = model.predict(features)[0]

        # Return result
        return jsonify({"prediction": int(prediction)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(port=5000)