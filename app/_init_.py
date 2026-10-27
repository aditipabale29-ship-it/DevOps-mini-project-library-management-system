from flask import Flask, jsonify

from app.routes.api import api


def create_app():
    app = Flask(__name__)

    app.register_blueprint(api)

    @app.route("/")
    def home():
        return jsonify({
            "message": "Library Management System",
            "status": "running"
        })

    return app
