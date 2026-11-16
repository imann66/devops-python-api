import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Task


def create_test_task(client):
    """Create a task through the API for use in integration tests."""
    response = client.post(
        "/tasks",
        json={
            "title": "Integration Test Task",
            "description": "Created for automated testing",
            "status": "pending"
        }
    )

    assert response.status_code == 201
    return response.get_json()


def test_create_task_persists_to_database(client, app):
    response = client.post(
        "/tasks",
        json={
            "title": "Pytest Integration Task",
            "description": "Verify persistence in PostgreSQL",
            "status": "pending"
        }
    )

    assert response.status_code == 201

    response_data = response.get_json()

    assert response_data["title"] == "Pytest Integration Task"
    assert response_data["status"] == "pending"

    with app.app_context():
        saved_task = db.session.get(Task, response_data["id"])

        assert saved_task is not None
        assert saved_task.title == "Pytest Integration Task"
        assert saved_task.description == (
            "Verify persistence in PostgreSQL"
        )
        assert saved_task.status == "pending"


def test_get_all_tasks(client):
    create_test_task(client)

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["title"] == "Integration Test Task"


def test_get_task_by_id(client):
    created_task = create_test_task(client)
    task_id = created_task["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == task_id
    assert response.get_json()["title"] == "Integration Test Task"


def test_update_task_persists_to_database(client, app):
    created_task = create_test_task(client)
    task_id = created_task["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated Integration Task",
            "status": "in_progress"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["title"] == "Updated Integration Task"
    assert response.get_json()["status"] == "in_progress"

    with app.app_context():
        saved_task = db.session.get(Task, task_id)

        assert saved_task.title == "Updated Integration Task"
        assert saved_task.status == "in_progress"


def test_delete_task_removes_from_database(client, app):
    created_task = create_test_task(client)
    task_id = created_task["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    with app.app_context():
        deleted_task = db.session.get(Task, task_id)

        assert deleted_task is None


def test_invalid_update_does_not_modify_database(client, app):
    created_task = create_test_task(client)
    task_id = created_task["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Should Not Be Saved",
            "status": "invalid_status"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid status."

    with app.app_context():
        saved_task = db.session.get(Task, task_id)

        assert saved_task.title == "Integration Test Task"
        assert saved_task.status == "pending"


def test_database_rejects_invalid_task_status(app):
    with app.app_context():
        with pytest.raises(IntegrityError):
            db.session.execute(
                text("""
                    INSERT INTO tasks (
                        title,
                        status,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :title,
                        :status,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                """),
                {
                    "title": "Invalid Status Test",
                    "status": "cancelled"
                }
            )

        db.session.rollback()

        result = db.session.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE title = :title
            """),
            {"title": "Invalid Status Test"}
        ).scalar_one()

        assert result == 0


def test_database_rejects_null_task_title(app):
    with app.app_context():
        with pytest.raises(IntegrityError):
            db.session.execute(
                text("""
                    INSERT INTO tasks (
                        title,
                        status,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        NULL,
                        'pending',
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                """)
            )

        db.session.rollback()

        result = db.session.execute(
            text("""
                SELECT COUNT(*)
                FROM tasks
                WHERE title IS NULL
            """)
        ).scalar_one()

        assert result == 0


def test_database_rejects_duplicate_primary_key(client, app):
    created_task = create_test_task(client)
    task_id = created_task["id"]

    with app.app_context():
        with pytest.raises(IntegrityError):
            db.session.execute(
                text("""
                    INSERT INTO tasks (
                        id,
                        title,
                        status,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :id,
                        :title,
                        :status,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                """),
                {
                    "id": task_id,
                    "title": "Duplicate ID Test",
                    "status": "pending"
                }
            )

        db.session.rollback()

        original_task = db.session.get(Task, task_id)

        assert original_task is not None
        assert original_task.title == "Integration Test Task"
