from flask import Flask
from flask_cors import CORS
from backend.app.routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
CORS(app)

#TODO: Hide this somehow idk
app.config["SECRET_KEY"] = "temp_key"