import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load model and encoder
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('encoder.pkl', 'rb') as encoder_file:
    encoder = pickle.load(encoder_file)

# Expected skills list
expected_skills = [
    'Database_Fundamentals', 'Computer_Architecture', 'Distributed_Computing_Systems', 
    'Cyber_Security', 'Networking', 'Software_Development', 'Programming_Skills', 
    'Project_Management', 'Computer_Forensics_Fundamentals', 'Technical_Communication', 
    'AI_ML', 'Software_Engineering', 'Business_Analysis', 'Communication_skills', 
    'Data_Science', 'Troubleshooting_skills', 'Graphics_Designing', 'Openness', 
    'Conscientousness', 'Extraversion', 'Agreeableness', 'Emotional_Range', 'Conversation', 
    'Openness_to_Change', 'Hedonism', 'Self-enhancement', 'Self-transcendence'
]

@app.route('/', methods=['POST'])
def predict():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")

        # Check for missing skills
        missing_skills = [skill for skill in expected_skills if skill not in data]
        if missing_skills:
            return jsonify({"error": f"Missing skills in input: {', '.join(missing_skills)}"}), 400

        # Extract skill values and validate numeric inputs
        try:
            skills = [float(data[skill]) for skill in expected_skills]
        except ValueError:
            return jsonify({"error": "All skill values must be numeric."}), 400

        # Prepare input for the model
        input_data = np.array(skills).reshape(1, -1)

        # Predict job role
        predicted_role_index = model.predict(input_data)[0]
        predicted_role = encoder.inverse_transform([predicted_role_index])[0]

        # Return result as JSON
        return jsonify({"predicted_role": predicted_role}), 200

    except Exception as e:
        # Log and return error message as JSON
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
