from flask import Blueprint, request, jsonify, g
from bson.objectid import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('/users/add', methods=['POST'])
def add_user():
    data = request.json
    if not all(k in data for k in ['name', 'email']):
        return jsonify({"error": "Missing name or email"}), 400
    result = g.mongo.db.users.insert_one({
        "name": data['name'],
        "email": data['email'],
        "roles": data.get('roles', [])
    })
    return jsonify({"userId": str(result.inserted_id), "status": "success"})

@user_bp.route('/users/<user_id>/assignRole', methods=['POST'])
def assign_role(user_id):
    data = request.json
    if 'roles' not in data:
        return jsonify({"error": "Missing roles"}), 400
    result = g.mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"roles": data['roles']}}
    )
    if result.matched_count:
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "User not found"}), 404
