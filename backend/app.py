from flask import Flask, request, render_template, jsonify
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo

# -----------------------------
# Load .env
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")

loaded = load_dotenv(dotenv_path)

print("Current directory:", os.getcwd())
print("Directory files:", os.listdir(BASE_DIR))
print("Loaded:", loaded)
print("Path:", dotenv_path)
print("File exists:", os.path.exists(dotenv_path))

MONGO_URI = os.getenv("MONGO_URI")
print("MONGO_URI =", MONGO_URI)

# -----------------------------
# MongoDB Connection
# -----------------------------
client = pymongo.MongoClient(MONGO_URI)
db = client.Test
collection = db["flask-tutorial"]

# -----------------------------
# Flask App
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    day_of_week = datetime.today().strftime("%A")
    current_time = datetime.now().strftime("%H:%M:%S")

    return render_template(
        "index.html",
        day_of_week=day_of_week,
        current_time=current_time
    )

# -----------------------------
# Submit Form
# -----------------------------
@app.route("/submit", methods=["POST"])
def submit():

    try:

        # If Express sends JSON
        form_data = request.get_json(silent=True)

        # If Browser sends Form Data
        if not form_data:
            form_data = dict(request.form)

        print("================================")
        print("Received Data:", form_data)
        print("================================")

        form_data["created_at"] = datetime.now()

        collection.insert_one(form_data)

        print("Inserted Successfully")

        return "Data submitted successfully!"

    except Exception as e:

        print("========== ERROR ==========")
        print(e)
        print("===========================")

        return str(e), 500

# -----------------------------
# View Data
# -----------------------------
@app.route("/view")
def view():

    data = list(collection.find())

    for item in data:
        item["_id"] = str(item["_id"])

    return jsonify(data)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)