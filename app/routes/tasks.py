
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import Task

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Title is required and must be a non-empty string."
        }), 400

    if len(title) > 150:
        return jsonify({
            "error": "Title must not exceed 150 characters."
        }), 400

    description = data.get("description")

    if description is not None and not isinstance(description, str):
        return jsonify({
            "error": "Description must be a string."
        }), 400

    status = data.get("status", "pending")

    if status not in ["pending", "in_progress", "completed"]:
        return jsonify({
            "error": "Invalid status."
        }), 400

    task = Task(
        title=title.strip(),
        description=description,
        status=status
    )

    try:
        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }), 201

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            "error": "Failed to create task."
        }), 500

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = Task.query.order_by(Task.id.asc()).all()

        return jsonify([
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]), 200

    except SQLAlchemyError:
        return jsonify({
            "error": "Failed to retrieve tasks."
        }), 500

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = db.session.get(Task, task_id)

        if task is None:
            return jsonify({
                "error": "Task not found."
            }), 404

        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }), 200

    except SQLAlchemyError:
        return jsonify({
            "error": "Failed to retrieve task."
        }), 500


@tasks_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    try:
        task = db.session.get(Task, task_id)

        if task is None:
            return jsonify({
                "error": "Task not found."
            }), 404

        # Validate all supplied fields before changing the task.
        new_title = None
        new_description = None
        new_status = None

        if "title" in data:
            new_title = data["title"]

            if not isinstance(new_title, str) or not new_title.strip():
                return jsonify({
                    "error": "Title must be a non-empty string."
                }), 400

            if len(new_title) > 150:
                return jsonify({
                    "error": "Title must not exceed 150 characters."
                }), 400

        if "description" in data:
            new_description = data["description"]

            if (
                new_description is not None
                and not isinstance(new_description, str)
            ):
                return jsonify({
                    "error": "Description must be a string."
                }), 400

        if "status" in data:
            new_status = data["status"]

            if new_status not in [
                "pending",
                "in_progress",
                "completed"
            ]:
                return jsonify({
                    "error": "Invalid status."
                }), 400

        # Apply changes only after all validations pass.
        if "title" in data:
            task.title = new_title.strip()

        if "description" in data:
            task.description = new_description

        if "status" in data:
            task.status = new_status

        db.session.commit()

        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }), 200

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            "error": "Failed to update task."
        }), 500


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task = db.session.get(Task, task_id)

        if task is None:
            return jsonify({
                "error": "Task not found."
            }), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "message": "Task deleted successfully."
        }), 200

    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({
            "error": "Failed to delete task."
        }), 500