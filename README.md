# FastAPI Starter: AWS & Kubernetes (EKS) Ready

A tiny FastAPI web app you can run locally, containerize with Docker, deploy to **AWS App Runner** first (fastest path),
and then (optionally) to **Amazon EKS (Kubernetes)**.

---

## 1) Run locally (no Docker)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export APP_ENV=local
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Open: http://localhost:8080

---

## 2) Docker: build & run

```bash
docker build -t fastapi-starter:latest .
docker run -p 8080:8080 -e APP_ENV=docker fastapi-starter:latest
```

Open: http://localhost:8080

---

## 3) Push to GitHub

1. Create a new repo on GitHub (public or private).
2. Initialize and push:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: FastAPI + Docker + K8s"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

The included GitHub Actions workflow (`.github/workflows/ci.yml`) runs tests and builds your container.
It includes commented steps to authenticate with AWS and push to Amazon ECR.

---

## 4) Fastest deploy path: AWS App Runner (from GitHub)

Why: App Runner builds & runs your container for you, manages scaling, HTTPS, and health checks—no infra to manage.

High-level steps:
1. In AWS Console → App Runner → Create service.
2. Source: Choose "Source code" → Connect your GitHub repo (first time needs authorization).
3. Build settings:
   - Runtime: Python or Dockerfile (recommended). If using Dockerfile, the default works out of the box.
   - Start command (if "Source code" & Python runtime): `uvicorn app.main:app --host 0.0.0.0 --port 8080`
4. Health check path: `/healthz`
5. Env var: `APP_ENV=apprunner`
6. CPU/RAM: start with the smallest.
7. Auto deployments: enable if you want new commits to redeploy automatically.

After it provisions, you'll get a public HTTPS URL.

Optional: Deploy from Amazon ECR instead of source code. Build/push locally or via CI, then point App Runner at your ECR image.

---

## 5) Optional: Kubernetes locally (minikube or kind)

Install one of:
- minikube: https://minikube.sigs.k8s.io/
- kind: https://kind.sigs.k8s.io/

Then:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
# For local ingress (requires ingress controller like ingress-nginx):
kubectl apply -f k8s/ingress.local.yaml
```

Open the address printed by your ingress controller (often http://demo.localtest.me once hosts/DNS are set up by the controller).

---

## 6) Optional: Amazon EKS (managed Kubernetes)

Easiest path: use eksctl.
- Install: https://eksctl.io/
- Create a cluster (example in ap-southeast-1 / Singapore):
  ```bash
  eksctl create cluster --name demo-fastapi --region ap-southeast-1 --nodes 2 --node-type t3.small
  ```
- Update kubeconfig:
  ```bash
  aws eks update-kubeconfig --name demo-fastapi --region ap-southeast-1
  ```
- Deploy app:
  ```bash
  kubectl apply -f k8s/deployment.yaml
  kubectl apply -f k8s/service.yaml
  ```
- Ingress: install AWS Load Balancer Controller and then:
  ```bash
  kubectl apply -f k8s/ingress.eks.yaml
  ```
This provisions an external Application Load Balancer for your service.

Cleanup (to avoid costs):
```bash
kubectl delete -f k8s/ingress.eks.yaml
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
eksctl delete cluster --name demo-fastapi --region ap-southeast-1
```

---

## 7) Env, secrets, and DBs

- Configure env vars in App Runner or Kubernetes. Example: `APP_ENV=prod`
- Secrets: use AWS Secrets Manager or SSM Parameter Store, or Kubernetes `Secret`.
- Databases: start with Amazon RDS (PostgreSQL/MySQL) or DynamoDB (serverless). For demos, SQLite works locally.

---

## 8) Test

```bash
pytest -q
```

---

## 9) Next steps

- Add a custom domain with HTTPS (App Runner supports this).
- Observability: CloudWatch logs & metrics. On EKS, consider Prometheus/Grafana.
- Autoscaling: App Runner scales automatically; on EKS use HPA.
- CI/CD: finalize ECR push via GitHub Actions with OIDC or access keys (prefer OIDC).