from flask import Flask, jsonify, request
app = Flask(__name__)

# Mock data for demonstration purposes
patients_data = {
    "1": {
        "name": "John Doe",
        "age": 30,
        "metrics": [
            {"type": "heart_rate", "value": 72, "timestamp": "2024-02-12T10:00:00"},
            {"type": "blood_pressure", "value": "120/80", "timestamp": "2024-02-12T10:05:00"},
        ]
    }
}

@app.route('/api/patient/<patientId>', methods=['GET'])
def get_patient_data(patientId):
    patient = patients_data.get(patientId)
    if patient:
        return jsonify(patient)
    else:
        return jsonify({"error": "Patient not found"}), 404

@app.route('/api/metrics/realtime/<patientId>', methods=['GET'])
def get_real_time_health_metrics(patientId):
    # This is a mock implementation. In a real scenario, you would fetch the latest metrics from your data source.
    latest_metrics = {"heart_rate": 75, "blood_pressure": "118/79"}
    return jsonify(latest_metrics)

@app.route('/api/metrics/history/<patientId>', methods=['GET'])
def get_historical_health_data(patientId):
    metricType = request.args.get('metricType')
    fromDate = request.args.get('fromDate')
    toDate = request.args.get('toDate')
    # In a real application, you would query your database or data storage based on these parameters.
    # This is a simplified example:
    history = {"data": "Historical data based on your query parameters"}
    return jsonify(history)

