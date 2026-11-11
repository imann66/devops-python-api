# DevOps Python API

A containerized REST API built with Python and Flask, demonstrating a practical DevOps workflow with automated testing, security scanning, continuous integration, Docker, and Kubernetes.

## Project Overview

This project demonstrates the journey from application development to containerized deployment.

The application is tested and scanned automatically through GitHub Actions. It is also deployed locally to a Kubernetes cluster using Kind.

## Architecture

```text
CI PIPELINE
───────────

Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Pytest
    ├── Bandit Security Scan
    ├── Docker Build
    └── Trivy Image Scan


LOCAL KUBERNETES DEPLOYMENT
───────────────────────────

Docker Image
    │
    ▼
Kind Kubernetes Cluster
    │
    ▼
Kubernetes Deployment
    │
    ├── Pod 1 ── Flask API
    │
    └── Pod 2 ── Flask API
            │
            ▼
     Kubernetes Service
            │
            ▼
 localhost:8080 (Port Forward)
```

## Technology Stack

| Category                | Technology     |
| ----------------------- | -------------- |
| Programming Language    | Python         |
| Web Framework           | Flask          |
| Testing                 | Pytest         |
| Containerization        | Docker         |
| CI                      | GitHub Actions |
| Code Security           | Bandit         |
| Container Security      | Trivy          |
| Container Orchestration | Kubernetes     |
| Local Kubernetes        | Kind           |
| Version Control         | Git and GitHub |

## Project Structure

```text
devops-python-api/
├── app/
│   ├── __init__.py
│   └── app.py
├── tests/
│   └── test_app.py
├── kubernetes/
│   ├── deployment.yml
│   └── service.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## API Endpoints

| Method | Endpoint  | Description                           |
| ------ | --------- | ------------------------------------- |
| GET    | `/`       | Returns an API status message         |
| GET    | `/health` | Returns the application health status |

Example response:

```json
{
  "message": "DevOps API is running"
}
```

Health check response:

```json
{
  "status": "healthy"
}
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/imann66/devops-python-api.git
cd devops-python-api
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements-dev.txt
```

### 4. Run the application

```powershell
python app/app.py
```

The application will be available at:

- `http://localhost:5000/`
- `http://localhost:5000/health`

### 5. Run tests

```powershell
python -m pytest -v
```

## Docker

### Build the image

```powershell
docker build -t devops-python-api:latest .
```

### Run the container

```powershell
docker run --rm -p 5000:5000 devops-python-api:latest
```

Test the health endpoint:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

## Continuous Integration

The GitHub Actions workflow automatically runs when code is pushed to the repository.

The pipeline performs the following steps:

1. Runs automated tests with Pytest.
2. Scans Python code using Bandit.
3. Builds the Docker image.
4. Scans the Docker image using Trivy.

The project was also tested by intentionally introducing a failing test and confirming that GitHub Actions stopped the pipeline. After fixing the test, the pipeline successfully passed again.

This verifies that the CI pipeline can detect broken application code.

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

The Deployment runs two replicas of the Flask application.

### 5. Create the Service

```powershell
kubectl apply -f kubernetes/service.yml
```

Verify the Service:

```powershell
kubectl get services
```

### 6. Access the application

Forward local port `8080` to the Kubernetes Service:

```powershell
kubectl port-forward service/devops-python-api-service 8080:5000
```

In another terminal, test the API:

```powershell
Invoke-RestMethod http://localhost:8080/
Invoke-RestMethod http://localhost:8080/health
```

## Health Checks

The Kubernetes Deployment uses both readiness and liveness probes.

Both probes call the `/health` endpoint.

- **Readiness probe:** Determines whether the application is ready to receive traffic.
- **Liveness probe:** Determines whether the application is still running correctly.

During deployment, a networking issue was identified because Flask was initially listening on `127.0.0.1`. The application was updated to listen on `0.0.0.0`, allowing Kubernetes health probes to reach the application through the Pod network.

## Key DevOps Concepts Demonstrated

- Git and GitHub version control
- Automated testing with Pytest
- Continuous Integration with GitHub Actions
- Python security scanning with Bandit
- Container vulnerability scanning with Trivy
- Docker containerization
- Kubernetes Deployments and replica management
- Kubernetes Services and networking
- Readiness and liveness probes
- Kubernetes rolling updates
- Container and Kubernetes troubleshooting

## Future Improvements

Possible improvements for the next version include:

- Use Gunicorn instead of Flask's development server.
- Publish Docker images to a container registry.
- Add automated Kubernetes deployment to the CI/CD pipeline.
- Add Kubernetes resource requests and limits.
- Add ConfigMaps and Secrets for application configuration.
- Add centralized logging and monitoring.

## Author

**Iman**

GitHub: https://github.com/imann66
