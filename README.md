# AKS Kubernetes Cluster - Bitcoin Service

## Table of Contents

1. [Project Overview](#project-overview)
2. [Build and Run Instructions](#build-and-run-instructions)
3. [Project Structure](#project-structure)
4. [Architecture](#architecture)
5. [Bitcoin API Used](#bitcoin-api-used)
6. [Ingress Access](#ingress-access)
7. [Contact](#contact)

---

## Project Overview

This repository contains Kubernetes manifests and Python applications designed to run on an Azure Kubernetes Service (AKS) cluster in the `creating-k8s` namespace. The cluster includes two services: Service-A and Service-B.

* **Service-A** fetches the Bitcoin price from an external API every minute and calculates the 10-minute average.
* **Service-B** is a simple Python service with a basic application.
* An Ingress Controller redirects traffic to the services via distinct paths.
* RBAC and NetworkPolicies are configured to restrict Service-A from accessing Service-B.

---

## Build and Run Instructions

### Prerequisites

* Azure CLI
* kubectl
* Docker
* GitHub CLI / Git
* Existing AKS Cluster with Ingress Controller installed

### Steps

1. Clone this repository:

```bash
git clone https://github.com/your-username/creating_k8s.git
cd creating_k8s
```

2. Build Docker images for both services:

```bash
cd service-a
docker build -t service-a:latest .
cd ../service-b
docker build -t service-b:latest .
```

3. Push images to Azure Container Registry (or Docker Hub):

```bash
az acr login --name <ACR_NAME>
docker tag service-a <ACR_NAME>.azurecr.io/service-a:latest
docker tag service-b <ACR_NAME>.azurecr.io/service-b:latest

docker push <ACR_NAME>.azurecr.io/service-a:latest
docker push <ACR_NAME>.azurecr.io/service-b:latest
```

4. Deploy Kubernetes manifests to AKS:

```bash
kubectl apply -f manifests/deny-a-to-b.yaml
kubectl apply -f manifests/service-a-deployment.yaml
kubectl apply -f manifests/service-a-service.yaml
kubectl apply -f manifests/service-b-deployment.yaml
kubectl apply -f manifests/service-b-service.yaml
kubectl apply -f manifests/ingress.yaml
```

5. Retrieve External IP for Ingress:

```bash
kubectl get ingress -n creating-k8s
```

---

## Project Structure

```
.
├── manifests/
│   ├── deny-a-to-b.yaml                # NetworkPolicy to block Service-A from talking to Service-B
│   ├── ingress.yaml                    # Ingress rules for URL routing
│   ├── service-a-deployment.yaml       # Deployment for Service-A
│   ├── service-a-service.yaml          # Service for Service-A
│   ├── service-b-deployment.yaml       # Deployment for Service-B
│   ├── service-b-service.yaml          # Service for Service-B
├── service-a/
│   ├── Dockerfile                      # Dockerfile for Service-A
│   └── main.py                         # Python app for fetching Bitcoin price
├── service-b/
│   ├── Dockerfile                      # Dockerfile for Service-B
│   └── main.py                         # Basic Python app
└── README.md
```

---

## Architecture

```
                   +---------------------------+
                   |     Ingress Controller     |
                   +---------------------------+
                        |               |
    /service-A --------->|               |<--------- /service-B
                        v               v
                  +-------------+   +-------------+
                  |  Service-A  |   |  Service-B  |
                  +-------------+   +-------------+
```

* Service-A fetches Bitcoin price and calculates the average.
* Service-A and Service-B cannot communicate directly (NetworkPolicy enforced).

---

## Bitcoin API Used

* **CoinGecko API:**
  `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd`

---

## Ingress Access

External access is provided via the Ingress Controller:

```
http://<EXTERNAL-IP>/service-A
http://<EXTERNAL-IP>/service-B
```

To get the external IP:

```bash
kubectl get ingress -n creating-k8s
```

---

## Contact

For any questions, please contact:
📧 [pz0933@gmail.com](mailto:pz0933@gmail.com)
