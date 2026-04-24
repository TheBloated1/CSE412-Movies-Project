from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from zoneinfo import ZoneInfo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    #TODO: Actual auth
    if username != "admin" or password != "123":
        return jsonify({
            "error": "Invalid credentials"
        }), 401
    #Create a token that expires in an hour
    token = jwt.encode(
        {
            "user_id": 1,
            "username": username,
            "exp": datetime.datetime.now(ZoneInfo("America/Phoenix")) + datetime.timedelta(hours=1)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    #Return with dummy info for now
    return jsonify({
        "token": token,
        "user": {
            "id": 1,
            "username": username
        }
    }),200