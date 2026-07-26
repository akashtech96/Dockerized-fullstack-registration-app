from flask import Flask, request, render_template, jsonify
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import pymongo
import re
import logging
from werkzeug.security import generate_password_hash

# -------------------------------------------------
# Flask App
# -------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------
# Logging Configuration
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Validation Patterns
# -------------------------------------------------
USERNAME_PATTERN = r"^[A-Za-z][A-Za-z0-9_]{2,19}$"

PASSWORD_PATTERN = (
    r"^(?=.*[a-z])"
    r"(?=.*[A-Z])"
    r"(?=.*\d)"
    r"(?=.*[@$!%*?&])"
    r"[A-Za-z\d@$!%*?&]{8,}$"
)

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")

loaded = load_dotenv(dotenv_path)

MONGO_URI = os.getenv("MONGO_URI")

logger.info("Loading environment variables...")
logger.info(f".env loaded: {loaded}")

if not MONGO_URI:
    logger.error("MONGO_URI is missing.")
    raise Exception("MONGO_URI is not configured.")

logger.info("MongoDB URI loaded successfully.")

# -------------------------------------------------
# MongoDB Connection
# -------------------------------------------------
try:

    client = pymongo.MongoClient(MONGO_URI)

    client.admin.command("ping")

    logger.info("Connected to MongoDB Atlas successfully.")

except Exception:

    logger.exception("Failed to connect to MongoDB.")

    raise

db = client.Test

collection = db["flask-tutorial"]

# -------------------------------------------------
# Home Route
# -------------------------------------------------
@app.route("/")
def home():

    day_of_week = datetime.today().strftime("%A")
    current_time = datetime.now().strftime("%H:%M:%S")

    return render_template(
        "index.html",
        day_of_week=day_of_week,
        current_time=current_time
    )

# -------------------------------------------------
# Registration Route
# -------------------------------------------------
@app.route("/submit", methods=["POST"])
def submit():

    try:

        form_data = request.get_json(silent=True)

        if not form_data:
            form_data = dict(request.form)

        username = form_data.get("name", "").strip()
        password = form_data.get("password", "").strip()

        # -----------------------------
        # Empty Validation
        # -----------------------------
        if not username or not password:

            return jsonify({

                "success": False,
                "error": "Username and Password are required."

            }), 400

        # -----------------------------
        # Username Validation
        # -----------------------------
        if not re.fullmatch(USERNAME_PATTERN, username):

            return jsonify({

                "success": False,
                "error": "Username must start with a letter and contain only letters, numbers or underscore (3-20 characters)."

            }), 400

        # -----------------------------
        # Password Validation
        # -----------------------------
        if not re.fullmatch(PASSWORD_PATTERN, password):

            return jsonify({

                "success": False,
                "error": "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character."

            }), 400

        # -----------------------------
        # Duplicate Username Check
        # -----------------------------
        existing_user = collection.find_one({

            "name": username

        })

        if existing_user:

            return jsonify({

                "success": False,
                "error": "Username already exists."

            }), 409

        # -----------------------------
        # Hash Password
        # -----------------------------
        hashed_password = generate_password_hash(password)

        # -----------------------------
        # User Document
        # -----------------------------
        user = {

            "name": username,
            "password": hashed_password,
            "created_at": datetime.now(timezone.utc)

        }

        collection.insert_one(user)

        logger.info(f"New user registered: {username}")

        return jsonify({

            "success": True,
            "message": "Registration completed successfully.",
            "user": username

        }), 201

    except Exception:

        logger.exception("Unexpected server error.")

        return jsonify({

            "success": False,
            "error": "Internal Server Error"

        }), 500

# -------------------------------------------------
# View Users
# -------------------------------------------------
@app.route("/view")
def view():

    users = list(collection.find())

    for user in users:

        user["_id"] = str(user["_id"])

    return jsonify(users)

# -------------------------------------------------
# Run Flask
# -------------------------------------------------
if __name__ == "__main__":

    app.run(

        host="0.0.0.0",
        port=5000,
        debug=False

    )