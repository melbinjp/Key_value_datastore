from flask import Flask, request, jsonify
from database import db, ma
from models import KeyValueStore
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

# JWT Setup
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
jwt = JWTManager(app)

# Example tenant login data
users = {
    'tenant1': 'password1',
    'tenant2': 'password2'
}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username not in users or users[username] != password:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/api/object', methods=['POST'])
@jwt_required()
def create_object():
    current_user = get_jwt_identity()
    data = request.get_json()
    key = data.get('key')
    value = data.get('data')
    ttl = data.get('ttl')

    if KeyValueStore.query.filter_by(key=key, tenant_id=current_user).first():
        return jsonify({"error": "Key already exists"}), 400

    ttl_time = datetime.utcnow() + timedelta(seconds=ttl) if ttl else None
    new_object = KeyValueStore(key=key, data=value, ttl=ttl_time, tenant_id=current_user)
    db.session.add(new_object)
    db.session.commit()
    return jsonify({"message": "Key-Value pair created"}), 201

@app.route('/api/object/<string:key>', methods=['GET'])
@jwt_required()
def get_object(key):
    current_user = get_jwt_identity()
    kv_object = KeyValueStore.query.filter_by(key=key, tenant_id=current_user).first()
    if not kv_object or kv_object.is_expired():
        return jsonify({"error": "Key not found or expired"}), 404

    return jsonify({"key": kv_object.key, "data": kv_object.data})

@app.route('/api/object/<string:key>', methods=['DELETE'])
@jwt_required()
def delete_object(key):
    current_user = get_jwt_identity()
    kv_object = KeyValueStore.query.filter_by(key=key, tenant_id=current_user).first()
    if not kv_object:
        return jsonify({"error": "Key not found"}), 404

    db.session.delete(kv_object)
    db.session.commit()
    return jsonify({"message": "Key-Value pair deleted"}), 200

@app.route('/api/batch/object', methods=['POST'])
@jwt_required()
def batch_create():
    current_user = get_jwt_identity()
    data = request.get_json()
    for item in data:
        key = item.get('key')
        value = item.get('data')
        ttl = item.get('ttl')

        if KeyValueStore.query.filter_by(key=key, tenant_id=current_user).first():
            continue

        ttl_time = datetime.utcnow() + timedelta(seconds=ttl) if ttl else None
        new_object = KeyValueStore(key=key, data=value, ttl=ttl_time, tenant_id=current_user)
        db.session.add(new_object)

    db.session.commit()
    return jsonify({"message": "Batch create complete"}), 201

# TTL expiration background job
def delete_expired_keys():
    with app.app_context():
        expired_objects = KeyValueStore.query.filter(KeyValueStore.ttl < datetime.utcnow()).all()
        for obj in expired_objects:
            db.session.delete(obj)
        db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_expired_keys, trigger="interval", seconds=60)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
