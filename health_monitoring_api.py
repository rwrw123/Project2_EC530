from flask import Flask, request, jsonify
from datetime import datetime, timezone
import logging
import json
from pymongo import MongoClient

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthMonitoringAPI")

class StructuredMessage:
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return f"{self.message} | {json.dumps(self.kwargs)}"

# MongoDB connection
client = MongoClient('localhost', 27017)
db = client['health_monitoring_db']

# MongoDB collections
users = db.users
devices = db.deviced
appointments = db.appointments
messages = db.messages
    
@app.route('/')
def index():
    """Root URL response."""
    return 'Health Monitoring API is running!'

@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.json
    if not all(k in data for k in ['name', 'email']):
        return jsonify({"error": "Missing name or email"}), 400
    user_id = users.insert_one({"name": data['name'], "email": data['email'], "roles": []}).inserted_id
    return jsonify({"userId": str(user_id), "status": "success"})

@app.route('/users/<int:user_id>/assignRole', methods=['POST'])
def assign_role(user_id):
    data = request.json
    if 'roles' not in data:
        return jsonify({"error": "Missing roles"}), 400
    result = users.update_one({"_id": user_id}, {"$set": {"roles": data['roles']}})
    if result.matched_count:
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/devices/register', methods=['POST'])
def register_device():
    data = request.json
    device_id = devices.insert_one({"deviceId": data['deviceId'], "type": data['type'], "status": "enabled"}).inserted_id
    return jsonify({"status": "success"})

@app.route('/patients/<int:patient_id>/measurements', methods=['POST'])
def submit_measurement(patient_id):
    data = request.json
    measurement_type = data['type']
    value = data.get('value')
    if value is None or not isinstance(value, (int, float)):
        return jsonify({"error": "Invalid measurement value"}), 400

    thresholds = {
        'bloodPressure': {'low': 90, 'high': 140},
        'temperature': {'low': 36.5, 'high': 37.5},
        'glucoseLevel': {'low': 70, 'high': 140},
    }

    if measurement_type in thresholds:
        threshold = thresholds[measurement_type]
        if not threshold['low'] <= value <= threshold['high']:
            generate_alert(patient_id, measurement_type, value, threshold)
            return jsonify({"status": "success", "alert": "Measurement outside of threshold"})
    else:
        return jsonify({"status": "success", "alert": "No threshold set for this measurement type"})

def generate_alert(patient_id, measurement_type, value, threshold):
    logger.info(StructuredMessage("ALERT",
                                   patient_id=patient_id,
                                   measurement_type=measurement_type,
                                   value=value,
                                   threshold=threshold))

@app.route('/patients/<patient_id>/appointments/book', methods=['POST'])
def book_appointment(patient_id):
    data = request.json
    appointment_id = appointments.insert_one({"patientId": patient_id, "mpId": data['mpId'], "time": data['time']}).inserted_id
    return jsonify({"appointmentId": str(appointment_id), "status": "success"})

@app.route('/patients/<patient_id>/appointments', methods=['GET'])
def view_appointments(patient_id):
    patient_appointments = list(appointments.find({"patientId": patient_id}))
    for appointment in patient_appointments:
        appointment['_id'] = str(appointment['_id'])  # Convert ObjectId to string
    return jsonify(patient_appointments)

@app.route('/chat/<patient_id>', methods=['POST'])
def post_message(patient_id):
    data = request.json
    message_id = messages.insert_one({"patientId": patient_id, "content": data['content'], "timestamp": datetime.now(timezone.utc).isoformat()}).inserted_id
    return jsonify({"status": "success"})

@app.route('/chat/<patient_id>', methods=['GET'])
def get_chat_history(patient_id):
    chat_history = list(messages.find({"patientId": patient_id }))
    for message in chat_history:
        message['_id'] = str(message['_id'])  # Convert ObjectId to string for JSON response
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(debug=True)
