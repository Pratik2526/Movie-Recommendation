from flask import Flask, request, jsonify
from rag_engine import MovieRAG
from db import (
    create_user,
    get_user_by_username,
    get_user_preferences,
    save_user_preference
)
from auth import create_token, decode_token
import uuid
import bcrypt

app = Flask(__name__)
rag = MovieRAG("movies_metadata.csv")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = bcrypt.hashpw(
        data["password"].encode(), bcrypt.gensalt()
    ).decode()

    user_id = str(uuid.uuid4())
    create_user(user_id, username, password)

    return jsonify({"message": "User registered successfully"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = get_user_by_username(data["username"])

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    user_id, hashed = user

    if not bcrypt.checkpw(data["password"].encode(), hashed.encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(user_id)
    return jsonify({"token": token})

@app.route("/chat", methods=["POST"])
def chat():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Missing token"}), 401

    user_id = decode_token(token.split(" ")[1])["user_id"]
    message = request.json["message"]

    preferences = get_user_preferences(user_id)

    if "i like" in message.lower():
        save_user_preference(user_id, message)
        preferences.append(message)

    enhanced_query = message + " " + " ".join(preferences)
    results = rag.search(enhanced_query)

    return jsonify({
        "movies": results["title"].tolist(),
        "memory": preferences
    })

if __name__ == "__main__":
    app.run(port=5000)
