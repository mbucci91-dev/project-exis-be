from flask import Flask
from models import db
from routes import api
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "super-secret-key"  
jwt = JWTManager(app)

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')