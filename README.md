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
## UI/UX Note

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
- The app will be available at: [http://127.0.0.1](http://127.0.0.1) or [http://loacalhost](http://localhost)

---

## Running on Minikube with HAProxy

1. Start Minikube:

```bash
minikube start --driver=docker 
```

2. Use Minikube’s Docker daemon:

```bash
eval $(minikube docker-env)
```

3. Build Docker images:

Ensure Docker is running and build all images:

```bash
# Build Mongo
docker build -t ttruc09/public-notes-mongo:latest -f mongo/Dockerfile ./mongo

# Build Flask Web App
docker build -t ttruc09/public-notes-app1:latest -f app/Dockerfile .

# Build HAProxy
docker build -t ttruc09/public-notes-haproxy:latest -f haproxy/Dockerfile ./haproxy
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
3. Get <MINIKUBE_IP>

```bash
minikube ip
```

4. Add host entry:

Edit your `/etc/hosts` file and add this line (replace IP accordingly):

```
<MINIKUBE_IP>    ttrinh.notes.com
```

5. Apply Ingress resource:

```bash
kubectl apply -f kubernetes-deployments/ingress.yaml
```

6. Start tunnel:

```bash
minikube tunnel
```

7. Visit in browser:

```
http://ttrinh.notes.com
```

---

## Troubleshooting

### Issue: Cannot access the web application using Minikube IP (e.g. `http://192.168.49.2`)

This may occur when running with **Ingress** due to local DNS resolution or routing conflicts on your machine.

### Solution:

If `http://<MINIKUBE_IP>` does **not** load the application, try the following:

1. **Use `localhost` instead:**

   You can directly access the app via:
   ```
   http://127.0.0.1
   ```

2. **Edit your `/etc/hosts` file (Linux/macOS) or `C:\Windows\System32\drivers\etc\hosts` (Windows):**

   Add the following line (replace IP if needed):

   ```
   127.0.0.1   ttrinh.notes.com
   ```

   Then, simply open:

   ```
   http://ttrinh.notes.com
   ```

3. **Make sure the tunnel is running:**

   ```
   minikube tunnel
   ```

   This is required when you're using **Ingress with Minikube**, as it routes external traffic into the cluster.

4. **Double-check Ingress Controller Port:**

   Run:

   ```bash
   kubectl get svc -n ingress-nginx
   ```

   Confirm that port `80` is mapped to a valid `NodePort` or handled correctly via the tunnel.
   
---

Still facing issues? Restart Ingress and reapply the manifests:

```bash
minikube addons disable ingress
minikube addons enable ingress
kubectl delete -f kubernetes-deployments/
kubectl apply -f kubernetes-deployments/
```
---
### Issue: ExitCode 14 / Restarting loop

**Cause:** MongoDB cannot write to the mounted data folder (`/data/db`).

### Solution

### If using bind mount (host folder) — platform-specific instructions:

#### Windows

1. Ensure the folder exists:
    ```powershell
    mkdir C:\Users\<your-user>\public-notes-platform\mongo-data
    ```

2. Share the folder with Docker:
    - Open **Docker Desktop** → **Settings** → **Resources** → **File Sharing**
    - Add:
      ```
      C:\Users\<your-user>\public-notes-platform\mongo-data
      ```
    - Click **Apply & Restart**



#### macOS or Linux

1. Ensure the folder exists:
    ```bash
    mkdir -p ~/public-notes-platform/mongo-data
    ```

2. Set proper permissions (MongoDB must have write access):
    ```bash
    chmod -R 777 ~/public-notes-platform/mongo-data
    ```

    > **Note:** Using `777` is suitable for local dev only. In production, use stricter permissions and user mapping.



### Alternative Fix: Use Docker **named volume**

Instead of bind mount, configure a named volume. In `docker-compose.yml`, replace:

```yaml
volumes:
  - ./mongo-data:/data/db
```

**With**

```yaml
volumes:
  - mongo-data:/data/db

volumes:
  mongo-data:
```

## Issue: HAProxy Cannot Resolve Backend DNS on Linux (EC2)

### Backend Resolution Fails on Linux (e.g., EC2)

When running on **Docker Desktop** (Windows/macOS), HAProxy can resolve backend service names (e.g., `app1`, `app2`) via Docker internal DNS on default port `80`.

However, on **Linux environments** (such as EC2), this resolution may fail. The HAProxy log will show errors like:

**[ALERT]** : 'server flask_backends/app1' : could not resolve address 'app1'.

### Solution:

Please kindly change from:

```yaml
backend flask_backends
    balance roundrobin
    server app1 app1:80 check
    server app2 app2:80 check
```

to:

```yaml
backend flask_backends
    balance roundrobin
    server app1 app1:5000 check
    server app2 app2:5000 check
```

Update in the file run.py:

```yaml
app.run(host="0.0.0.0", port=5000)
```

Rebuild Haproxy:

```yaml
docker compose up -d --build haproxy
```

Verify Runnning Container 

```yaml
docker ps
```

### Full Cleanup & Rebuild (When Things Go Wrong)

If HAProxy or any other service still fails after applying the basic troubleshooting steps, it's best to **clean up the environment completely** and perform a **full rebuild without using Docker cache**.

---

### Common Symptoms
- HAProxy still fails to resolve DNS
- Containers are not reachable or crash at startup
- Persistent volumes cause permission issues (especially on EC2/Linux)
- MongoDB container fails to start due to inaccessible data directory

---

### Solution: Full Reset & Clean Build

#### Stop All Containers, Remove Orphaned Volumes And Build Again Without Cache

```bash
# 1. Stop all containers and prune everything
docker compose down -v --remove-orphans
docker system prune -f --volumes

# 2. Fix local volume permission issues (Linux/EC2)
sudo rm -rf ~/public-notes-platform/mongo-data
mkdir -p ~/public-notes-platform/mongo-data
sudo chown -R ec2-user:ec2-user ~/public-notes-platform/mongo-data

# 3. Rebuild images without cache
docker compose build --no-cache

# 4. Start containers
docker compose up -d
```


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


