from database import db
from datetime import datetime

class KeyValueStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), unique=True, nullable=False)
    data = db.Column(db.JSON, nullable=False)
    ttl = db.Column(db.DateTime, nullable=True)
    tenant_id = db.Column(db.String(32), nullable=False)

    def is_expired(self):
        return self.ttl and datetime.utcnow() > self.ttl
