from flask import Blueprint, request, jsonify, g
from datetime import datetime, timezone

device_bp = Blueprint('device', __name__)

@device_bp.route('/devices/register', methods=['POST'])
def register_device():
    data = request.json
    result = g.mongo.db.devices.insert_one({
        "type": data['type'],
        "model": data['model'],
        "registration_date": datetime.now(timezone.utc)
    })
    return jsonify({"deviceId": str(result.inserted_id), "status": "success"})

