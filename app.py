from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# DATABASE
def get_db():
    conn = sqlite3.connect("smartattend.db")
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLES
conn = get_db()

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()

# HOME ROUTE
@app.route("/")
def home():
    return "SmartAttend Backend Running"

# REGISTER ROUTE
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    conn = get_db()

    conn.execute(
        "INSERT INTO users (name,email,password) VALUES (?,?,?)",
        (name, email, password)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Registration successful"
    })

# RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
