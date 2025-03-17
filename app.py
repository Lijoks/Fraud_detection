from flask import Flask, request, jsonify  
import numpy as np  
import joblib  
import pandas as pd  

# Initialize Flask app  
app = Flask(__name__)  

# Load the model, scaler, and feature names from disk  
model = joblib.load('credit_card_fraud_model.pkl')  
scaler = joblib.load('credit_card_fraud_scaler.pkl')  
feature_names = joblib.load('feature_names.pkl')  # Load feature names  
print(feature_names)  
print("Model and scaler loaded in API.")  

@app.route('/features', methods=['GET'])  
def get_features():  
    return jsonify({'features': feature_names.tolist()})  # Return feature names as a JSON response  

@app.route('/predict', methods=['POST'])  
def predict():  
    # Get data from the request  
    data = request.get_json(force=True)  

    # Ensure the input is a list of records  
    try:  
        input_df = pd.DataFrame(data)  
    except Exception as e:  
        return jsonify({'error': 'Incorrect input format. Please send a JSON list of records.', 'message': str(e)})  

    # Check that required features are present in the DataFrame  
    required_features = feature_names  # Use the stored feature names directly  

    if not all(feature in input_df.columns for feature in required_features):   
        return jsonify({  
            'error': 'Missing one or more required features.',  
            'required_features': required_features.tolist()  # Convert to list  
})   

    # Scale the input features  
    try:  
        print("Data for scaling:", input_df[required_features])  # Debugging output  
        input_scaled = scaler.transform(input_df[required_features])  # Scale only the relevant features  
    except Exception as e:  
        print(f"Error scaling features: {e}")  
        return jsonify({'error': 'Error during scaling of input data.', 'message': str(e)})  

    # Predict using the loaded model  
    try:  
        predictions = model.predict(input_scaled)  
        predictions_proba = model.predict_proba(input_scaled)[:, 1]  # Probability of the positive class  
    except Exception as e:  
        return jsonify({'error': 'Error during prediction.', 'message': str(e)})  

    # Return the output as a JSON object  
    results = []  
    for pred, proba in zip(predictions, predictions_proba):  
        results.append({  
            'prediction': int(pred),  
            'fraud_probability': float(proba)  
        })  

    return jsonify(results)  

if __name__ == '__main__':  
    app.run(debug=True)  