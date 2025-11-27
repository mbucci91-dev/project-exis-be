from flask import Flask, jsonify
from models import db, User, Card, Movement

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"status": "Backend separato correttamente!"})

@app.route("/api/users")
def get_users():
    all_users = User.query.all()
    
    users_list = []
    for user in all_users:
        users_list.append({
            "id": user.id, 
            "username": user.username
        })
        
    return jsonify(users_list)