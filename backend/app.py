from flask import Flask
from flask_cors import CORS

from db import init_db

from routes.auth_routes import auth_bp
from routes.url_routes import url_bp


app = Flask(__name__)

CORS(app)

# initialize database
init_db()

# register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(url_bp)


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/")
def home():
    return {
        "message": "Backend is running"
    }


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)