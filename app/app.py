
from flask import Flask, jsonify
from sqlalchemy import text

from app.config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.models import Task
    from app.routes.tasks import tasks_bp

    app.register_blueprint(tasks_bp)

    @app.route("/")
    def home():
        return jsonify({
            "message": "DevOps API is running"
        })

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy"
        })

    @app.route("/db-health")
    def db_health():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            return jsonify({
                "database": "healthy"
            }), 200

        except Exception:
            app.logger.exception("Database health check failed")

            return jsonify({
                "database": "unhealthy"
            }), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # nosec B104
