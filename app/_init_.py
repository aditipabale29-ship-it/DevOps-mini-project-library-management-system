from flask import Flask, jsonify

from app.routes.api import api
from app.routes.web import web


def create_app():
    app = Flask(__name__)

    app.register_blueprint(api)
    app.register_blueprint(web)

    @app.route("/")
    def home():
        return jsonify({
            "message": "Library Management System",
            "status": "running"
        })

    return app
