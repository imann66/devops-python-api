# DevOps Python API

A containerized Task Management REST API built with Python, Flask, and PostgreSQL. This project demonstrates practical DevOps and QA engineering workflows, including REST API development, automated testing, database integration, security scanning, continuous integration, Docker, and Kubernetes.

## Project Overview

This project demonstrates the software delivery lifecycle, from application development and database integration to containerization and Kubernetes deployment.

The application provides CRUD (Create, Read, Update, Delete) operations for task management. PostgreSQL is used for persistent data storage, while SQLAlchemy handles database interactions.

The project also incorporates:

- Automated API and database integration testing with Pytest.
- API validation and error handling.
- Database constraints and transaction testing.
- Continuous Integration using GitHub Actions.
- Python security scanning with Bandit.
- Docker image vulnerability scanning with Trivy.
- Containerization using Docker.
- Local Kubernetes deployment using Kind.

## Architecture

### CI Pipeline

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +-- PostgreSQL Service
    |
    +-- Pytest
    |     |
    |     +-- Application Tests
    |     +-- Database Integration Tests
    |
    +-- Bandit Security Scan
    |
    v
Docker Build and Security Job
    |
    +-- Docker Image Build
    |
    +-- Trivy Image Scan
```

### Application Architecture

```text
Client
  |
  v
Flask REST API
  |
  v
SQLAlchemy
  |
  v
PostgreSQL Database
  |
  v
Tasks Table
```

### Local Kubernetes Deployment

```text
Docker Image
    |
    v
Kind Kubernetes Cluster
    |
    v
Kubernetes Deployment
    |
    +-- Pod 1 -- Flask API
    |
    +-- Pod 2 -- Flask API
             |
             v
      Kubernetes Service
             |
             v
    localhost:8080
    (Port Forward)
```

The Kubernetes deployment demonstrates the containerized API deployment. PostgreSQL connectivity must be configured separately before database-backed endpoints can be used in Kubernetes.

## Technology Stack

| Category                | Technology          |
| ----------------------- | ------------------- |
| Programming Language    | Python 3.12         |
| Web Framework           | Flask               |
| ORM                     | Flask-SQLAlchemy    |
| Database                | PostgreSQL 16       |
| Database Driver         | Psycopg 3           |
| Configuration           | python-dotenv       |
| API Testing             | Postman             |
| Automated Testing       | Pytest              |
| Integration Testing     | Pytest + PostgreSQL |
| Code Security           | Bandit              |
| Containerization        | Docker              |
| CI                      | GitHub Actions      |
| Container Security      | Trivy               |
| Container Orchestration | Kubernetes          |
| Local Kubernetes        | Kind                |
| Version Control         | Git and GitHub      |

## Project Structure

```text
devops-python-api/
|
+-- app/
|   +-- __init__.py
|   +-- app.py
|   +-- config.py
|   +-- extensions.py
|   +-- models.py
|   |
|   +-- routes/
|       +-- tasks.py
|
+-- tests/
|   +-- conftest.py
|   +-- test_app.py
|   |
|   +-- integration/
|       +-- test_tasks_api.py
|
+-- kubernetes/
|   +-- deployment.yml
|   +-- service.yml
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml
|
+-- .dockerignore
+-- .gitignore
+-- .env.example
+-- Dockerfile
+-- create_tables.py
+-- requirements.txt
+-- requirements-dev.txt
+-- README.md
```

## API Endpoints

The application exposes the following endpoints:

| Method | Endpoint      | Description                   |
| ------ | ------------- | ----------------------------- |
| GET    | `/`           | Returns an API status message |
| GET    | `/health`     | Checks application health     |
| GET    | `/db-health`  | Checks database connectivity  |
| POST   | `/tasks`      | Creates a new task            |
| GET    | `/tasks`      | Retrieves all tasks           |
| GET    | `/tasks/<id>` | Retrieves a task by ID        |
| PATCH  | `/tasks/<id>` | Partially updates a task      |
| DELETE | `/tasks/<id>` | Deletes a task                |

### Example: Create a Task

Request:

```http
POST /tasks
Content-Type: application/json
```

```json
{
  "title": "Learn API Testing",
  "description": "Practice API testing with Postman",
  "status": "pending"
}
```

The API returns `201 Created` when the task is successfully created.

### Supported Task Statuses

- `pending`
- `in_progress`
- `completed`

### API Validation

The application validates incoming requests, including:

- Required task title.
- Non-empty title.
- Maximum title length of 150 characters.
- Description data type.
- Valid task status.
- Valid JSON request body.

The API also handles missing task records and database errors.

## Database Design

PostgreSQL is used to store task records.

### Tasks Table

| Column      | Data Type    | Constraint  |
| ----------- | ------------ | ----------- |
| id          | Integer      | Primary Key |
| title       | VARCHAR(150) | NOT NULL    |
| description | TEXT         | Nullable    |
| status      | VARCHAR(20)  | NOT NULL    |
| created_at  | TIMESTAMP    | NOT NULL    |
| updated_at  | TIMESTAMP    | NOT NULL    |

The database enforces a CHECK constraint to restrict task status values to:

```sql
CHECK (
    status IN (
        'pending',
        'in_progress',
        'completed'
    )
)
```

Additional database integrity rules include:

- Primary key uniqueness.
- NOT NULL constraints.
- Transaction rollback behavior.
- Atomicity when a transaction fails.

### Database Configuration

The application uses environment variables to configure database connectivity.

Create a local environment file using the example:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your local PostgreSQL credentials.

Example configuration:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=devops_api
DB_USER=postgres
DB_PASSWORD=your_local_password

TEST_DB_NAME=devops_api_test
```

The `.env` file is excluded from Git.

**Important:** Never commit real database credentials to the repository.

## Run Locally

### 1. Clone the repository

```powershell
git clone https://github.com/imann66/devops-python-api.git

cd devops-python-api
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements-dev.txt
```

### 4. Configure environment variables

```powershell
Copy-Item .env.example .env
```

Update `.env` with your PostgreSQL credentials.

Create the development database in PostgreSQL if it does not already exist:

```sql
CREATE DATABASE devops_api;
```

The application also requires a separate test database named `devops_api_test` for automated integration tests.

### 5. Create database tables

From the project root:

```powershell
python create_tables.py
```

### 6. Run the application

```powershell
python -m app.app
```

The API will be available at:

- http://localhost:5000/
- http://localhost:5000/health
- http://localhost:5000/db-health

## Automated Testing

Pytest is used to execute automated application and database integration tests.

### Run all tests

```powershell
python -m pytest -v
```

### Test Coverage

The current automated test suite includes:

**Application tests**

- Home endpoint.
- Application health endpoint.

**Database integration tests**

- Creating and persisting a task.
- Retrieving all tasks.
- Retrieving a task by ID.
- Updating a task.
- Deleting a task.
- Preventing invalid updates from modifying database records.
- Database rejection of invalid task status.
- Database rejection of NULL task titles.
- Database rejection of duplicate primary keys.

### Test Database Isolation

Automated integration tests use a separate PostgreSQL database:

```text
Development Database: devops_api
Test Database:        devops_api_test
```

The test fixtures recreate the test database tables before and after each test.

**Warning:** The test fixture drops and recreates tables in the configured test database. Never configure `TEST_DB_NAME` to point to a database containing development or production data.

### Current Test Results

Latest local test execution:

```text
11 passed in 0.52s
```

All 11 automated tests passed.

## Manual API Testing

Postman was used to validate the REST API before and alongside automated testing.

Testing included:

- Successful CRUD operations.
- Invalid request payloads.
- Missing required fields.
- Invalid task statuses.
- Non-existent task IDs.
- Complete end-to-end CRUD workflow.
- API responses compared against PostgreSQL records.

Database verification was performed using SQL queries to confirm that API operations correctly affected persistent records.

## Docker

The application is containerized using Docker.

### Build the image

```powershell
docker build -t devops-python-api:latest .
```

### Run the container

The application requires database configuration at runtime. Provide the environment variables through an environment file:

```powershell
docker run --rm -p 5000:5000 --env-file .env devops-python-api:latest
```

When connecting to PostgreSQL running directly on the Windows host from Docker Desktop, use `host.docker.internal` as the database host instead of `localhost`.

For example:

```env
DB_HOST=host.docker.internal
```

The PostgreSQL server must allow connections from the Docker container.

Test the application:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

Check database connectivity:

```powershell
Invoke-RestMethod http://localhost:5000/db-health
```

## Continuous Integration and Security

GitHub Actions automates application testing and security checks.

The workflow is triggered by pushes and pull requests targeting the `main` branch for pull requests.

### Job 1: Test and Code Security

The workflow:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Starts a temporary PostgreSQL 16 service container.
4. Installs project and development dependencies.
5. Runs automated tests using Pytest.
6. Scans Python application code using Bandit.

### Job 2: Docker Build and Security

This job runs after the test and code security job succeeds.

The workflow:

1. Checks out the repository.
2. Builds the Docker image.
3. Scans the image using Trivy.
4. Reports HIGH and CRITICAL vulnerability findings.

The current Trivy configuration uses `exit-code: "0"`, so vulnerability findings are reported but do not independently fail the workflow.

### CI Database Configuration

The CI pipeline uses disposable credentials for its temporary PostgreSQL service.

These values are intentionally configured in the workflow:

```text
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
TEST_DB_NAME=devops_api_test
```

These credentials are intended exclusively for the isolated CI database.

They must never be reused for development or production databases.

Real local database credentials are kept in `.env`, which is excluded from Git.

### Pipeline Failure Validation

The pipeline was previously tested by intentionally introducing a failing test.

GitHub Actions correctly detected the failure and stopped the subsequent dependent job.

After the failing test was corrected, the pipeline successfully passed again.

This demonstrates that the CI workflow can detect application test failures and prevent the Docker security job from running when the preceding job fails.

## Security Practices

The project incorporates several security practices:

- Environment-based database configuration.
- `.env` excluded from version control.
- Separate development and test databases.
- Input validation for API requests.
- Database integrity constraints.
- SQLAlchemy transaction handling and rollback.
- Python security scanning with Bandit.
- Container vulnerability scanning with Trivy.

### Bandit Security Scan Exception

The Flask application listens on `0.0.0.0` so that it can receive connections through Docker and Kubernetes networking.

Bandit identifies binding to all interfaces under rule `B104`.

This behavior is intentional for the containerized application, so the specific finding is suppressed:

```python
app.run(host="0.0.0.0", port=5000)  # nosec B104
```

Only the specified finding on this line is suppressed. The remaining Bandit security checks stay active.

## Kubernetes Deployment

This project uses Kind to run Kubernetes locally.

### 1. Create the cluster

```powershell
kind create cluster --name devops-lab
```

Verify the cluster:

```powershell
kubectl get nodes
```

### 2. Build the Docker image

```powershell
docker build -t devops-python-api:latest .
```

### 3. Load the image into Kind

```powershell
kind load docker-image devops-python-api:latest --name devops-lab
```

### 4. Deploy the application

```powershell
kubectl apply -f kubernetes/deployment.yml
```

Verify the deployment:

```powershell
kubectl get deployments
kubectl get pods
```

Wait for the deployment:

```powershell
kubectl rollout status deployment/devops-python-api
```

The Deployment runs two replicas of the Flask application.

### 5. Create the Service

```powershell
kubectl apply -f kubernetes/service.yml
```

Verify the Service:

```powershell
kubectl get services
```

Inspect the EndpointSlices:

```powershell
kubectl get endpointslices
```

### 6. Access the application

Forward local port `8080` to the Kubernetes Service:

```powershell
kubectl port-forward service/devops-python-api-service 8080:5000
```

Keep this terminal running.

In another terminal, test the API:

```powershell
Invoke-RestMethod http://localhost:8080/
Invoke-RestMethod http://localhost:8080/health
```

The database-backed task endpoints require a reachable PostgreSQL instance and appropriate database configuration in Kubernetes. That configuration is a separate deployment improvement.

## Health Checks and Troubleshooting

The Kubernetes Deployment uses readiness and liveness probes.

Both probes call the `/health` endpoint.

- **Readiness probe:** Determines whether the application is ready to receive traffic.
- **Liveness probe:** Determines whether the application is still running correctly.

During the initial Kubernetes deployment, the Pods were running but failed their health probes.

The issue was caused by Flask listening only on `127.0.0.1`, preventing Kubernetes from reaching the application through the Pod network.

The application was updated to listen on `0.0.0.0`, after which the Deployment successfully completed with two healthy replicas.

The troubleshooting process involved:

1. Inspecting Pod logs.
2. Using `kubectl describe pod` to investigate failed probes.
3. Identifying the application network binding issue.
4. Updating the Flask host configuration.
5. Rebuilding and loading the Docker image into Kind.
6. Restarting the Kubernetes Deployment.
7. Verifying two healthy Pods and successful API responses.

## Key Skills Demonstrated

- Python application development.
- REST API design and CRUD implementation.
- PostgreSQL database management.
- SQLAlchemy ORM.
- API testing with Postman.
- Automated testing with Pytest.
- Database integration testing.
- SQL database integrity and transaction testing.
- Git and GitHub version control.
- Continuous Integration with GitHub Actions.
- Python security scanning with Bandit.
- Container vulnerability scanning with Trivy.
- Docker image creation and container execution.
- Kubernetes Deployments and replica management.
- Kubernetes Services and networking.
- Readiness and liveness probes.
- Kubernetes rolling updates.
- Container and Kubernetes troubleshooting.
- Environment-based configuration management.

## Future Improvements

Potential improvements include:

- Add test coverage reporting.
- Introduce Gunicorn as the production WSGI server.
- Add automated API documentation using OpenAPI/Swagger.
- Add automated UI or end-to-end testing.
- Publish Docker images to a container registry.
- Add automated Kubernetes deployment to the CI/CD pipeline.
- Configure PostgreSQL connectivity in Kubernetes.
- Add Kubernetes resource requests and limits.
- Introduce ConfigMaps and Secrets for Kubernetes configuration.
- Add centralized logging and monitoring.
- Improve Trivy vulnerability enforcement.

## Author

**Iman**

GitHub: https://github.com/imann66
