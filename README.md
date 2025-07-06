# Public Notes Platform

## Overview

This is a simple web-based note management application built for the **Cloud Computing SS2025 Project**. It allows users to:

- **Search notes** by entering an email or a tag.
- **Add new notes**, associating them with an email and one or more tags.

There are two core pages in the web app:

1. **Home Page**  
   - Users can search for notes using **email** or **tags**.
   - Results (if any) are displayed below the input field.

2. **Create Note Page**  
   - Accessed by clicking the **“Add New Notes”** button on the home page.
   - Allows users to enter:
     - The **email** of the note owner.
     - The **tag(s)** used to categorize the note.
     - The **note content** itself.
   - Submitting the form will store the note in MongoDB.

---
## 📱 UI/UX Note

The web interface is **intentionally designed as a mobile web application**, optimized for smartphone screens.

To **best experience the interface**:

1. Open the app in **Google Chrome**.
2. Right-click anywhere → **Inspect**.
3. Toggle device toolbar (or press `Ctrl+Shift+M`).
4. Choose **“iPhone 14”** or similar from the device dropdown.
5. Refresh the page to simulate the intended mobile layout.

---
## Prerequisites

Make sure the following are properly installed and set up before running this project:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

---

## Running with Docker Compose

```bash
docker compose up --build -d
```

- Containers for web app and MongoDB will be built and deployed.
- The app will be available at: [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## Running on Minikube with HAProxy

1. Start Minikube:

```bash
minikube start
```

2. Use Minikube’s Docker daemon:

```bash
eval $(minikube docker-env)
```

3. Build Docker images:

```bash
# Build and load Mongo
docker build -t ttruc09/public-notes-mongo:latest -f mongo/Dockerfile .

# Build and load Flask Web App
docker build -t ttruc09/public-notes-app1:latest -f app/Dockerfile .

# Build and load HAProxy
docker build -t ttruc09/public-notes-haproxy:latest -f haproxy/Dockerfile .
```
4. Load Docker Images into Minikube:

if using Minikube with Docker driver

```bash
# Load Mongo
minikube image load ttruc09/public-notes-mongo:latest


# Load Flask Web App
minikube image load ttruc09/public-notes-app1:latest


# Load HAProxy
minikube image load ttruc09/public-notes-haproxy:latest

```
5. Deploy the app to Kubernetes:

```bash
kubectl apply -f kubernetes-deployments/
```

Wait a few moments, then check everything is running:

```bash
kubectl get pods
kubectl get svc
kubectl get ingress
```

6. Get access URL through HAProxy:

```bash
minikube service haproxy-service --url
```

---

## Running on Minikube with Ingress

1. Enable Ingress addon:

```bash
minikube addons enable ingress
```

2. Remove HAProxy resources if applied:

```bash
kubectl delete deployment haproxy-deployment
kubectl delete service haproxy-service
kubectl delete configmap haproxy-config
```

3. Add host entry:

Edit your `/etc/hosts` file and add this line (replace IP accordingly):

```
<MINIKUBE_IP>    ttrinh.notes.com
```

4. Apply Ingress resource:

```bash
kubectl apply -f kubernetes-deployments/ingress.yaml
```

5. Start tunnel:

```bash
minikube tunnel
```

6. Visit in browser:

```
http://ttrinh.notes.com
```

---



---

## Clean Up

To stop and delete all resources:

```bash
kubectl delete -f kubernetes-deployments/
```

To tear down Docker Compose:

```bash
docker compose down
```

---


