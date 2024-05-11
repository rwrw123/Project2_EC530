from flask import Blueprint, request, jsonify, g
from datetime import datetime, timezone

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patients/<int:patient_id>/measurements/add', methods=['POST'])
def submit_measurement(patient_id):
    data = request.json
    g.mongo.db.measurements.insert_one({
        "patient_id": patient_id,
        "type": data['type'],
        "value": data.get('value'),
        "timestamp": datetime.now(timezone.utc)
    })
    return jsonify({"status": "success"})

@patient_bp.route('/patients/<int:patient_id>/appointments/book', methods=['POST'])
def book_appointment(patient_id):
    data = request.json
    result = g.mongo.db.appointments.insert_one({
        "patient_id": patient_id,
        "mp_id": data['mpId'],
        "time": data['time']
    })
    return jsonify({"appointmentId": str(result.inserted_id), "status": "success"})
