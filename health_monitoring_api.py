from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime, timezone
import logging
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/health_db"
mongo = PyMongo(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthMonitoringAPI")

class StructuredMessage:
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return f"{self.message} | {json.dumps(self.kwargs)}"
    
@app.route('/')
def index():
    """Root URL response."""
    return 'Health Monitoring API is running!'

@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.json
    if not all(k in data for k in ['name', 'email']):
        return jsonify({"error": "Missing name or email"}), 400
    result = mongo.db.users.insert_one({
        "name": data['name']
        "email": data['email']
        "roles": []
    })
    return jsonify({"userId": str(result.inserted_id), "status": "success"})

@app.route('/users/<user_id>/assignRole', methods=['POST'])
def assign_role(user_id):
    data = request.json
    if 'roles' not in data:
        return jsonify({"error": "Missing roles"}), 400
    result = mongo.db.users.update_one({"_id": user_id}, {"$set": {"roles": data['roles']}})
    if result.matched_count:
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/devices/register', methods=['POST'])
def register_device():
    data = request.json
    result = mongo.db.devices.insert_one({"deviceId": data['deviceId'], "type": data['type'], "registration_date": datetime.now(timezone.utc)})
    return jsonify({"deviceId";str(result.inserted_id), "status": "success"})

@app.route('/patients/<int:patient_id>/measurements/add', methods=['POST'])
def submit_measurement(patient_id):
    data = request.json
    measurement_type = data['type']
    value = data.get('value')
    mongo.db.measurements.insert_one({
        "patient_id": patient_id,
        "type": measurement_type,
        "value" : value,
        "timestamp": datetime.now(timezone.utc)
    })
    return jsonify({"status": "success"})

@app.route('/patients/<int:patient_id>/appointments/book', methods=['POST'])
def book_appointment(patient_id):
    data = request.json
    result = mongo.db.appointments.insert_one({
        "patient_id": patient_id,
        "mp_id": data['mpId'],
        "time": data['time']
    })
    return jsonify({"appointmentId": str(result.inserted_id), "status": "success"})

@app.route('/patients/<int:patient_id>/appointments', methods=['GET'])
def view_appointments(patient_id):
    patient_appointments = list(mongo.db.appointments.find({"patient_id": patient_id}))
    return jsonify(patient_appointments)

@app.route('/chat/<int:patient_id>', methods=['POST'])
def post_message(patient_id):
    data = request.json
    message = {
        "patient_id": patient_id,
        "content": data['content'],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    mongo.db.messages.insert_one(message)
    return jsonify({"status": "success"})

@app.route('/chat/<int:patient_id>', methods=['GET'])
def get_chat_history(patient_id):
    chat_history = list(mongo.db.messages.find({"patient_id": patient_id}))
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(debug=True)
