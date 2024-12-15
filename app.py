import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Load model and encoder
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('encoder.pkl', 'rb') as encoder_file:
    encoder = pickle.load(encoder_file)

@app.route('/', methods=['POST'])
def predict():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # List of expected skills
        expected_skills = [
            'Database_Fundamentals', 'Computer_Architecture', 'Distributed_Computing_Systems', 
            'Cyber_Security', 'Networking', 'Software_Development', 'Programming_Skills', 
            'Project_Management', 'Computer_Forensics_Fundamentals', 'Technical_Communication', 
            'AI_ML', 'Software_Engineering', 'Business_Analysis', 'Communication_skills', 
            'Data_Science', 'Troubleshooting_skills', 'Graphics_Designing', 'Openness', 
            'Conscientousness', 'Extraversion', 'Agreeableness', 'Emotional_Range', 'Conversation', 
            'Openness_to_Change', 'Hedonism', 'Self-enhancement', 'Self-transcendence'
        ]

        # Extract skill values from JSON data
        skills = [float(data[skill]) for skill in expected_skills]

        # Prepare input for the model
        input_data = np.array(skills).reshape(1, -1)

        # Predict job role
        predicted_role_index = model.predict(input_data)[0]
        predicted_role = encoder.inverse_transform([predicted_role_index])[0]

        # Return result as JSON
        return jsonify({"predicted_role": predicted_role})

    except Exception as e:
        # Return error message as JSON
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
