# Public Notes Platform

## Overview

A simple Flask + MongoDB web app to create and search notes by email or tags. Deployed with Docker Compose (HAProxy + 2 app replicas) or Kubernetes (Minikube) with HAProxy/Ingress.

Features:
- Search notes by email or tags (#tag)
- Create notes with email, tags, content

Pages:
- Home: search by email or tag, show results
- Create Note: add new note (stored in MongoDB)

---
## UI/UX

Mobile-first UI (optimized for small screens). For best preview in Chrome: DevTools → Toggle Device Toolbar → iPhone 14 (refresh).

---
## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) + [kubectl](https://kubernetes.io/docs/tasks/tools/)

---

## 1. Run with Docker Compose

```bash
docker compose up --build -d
```

App: http://127.0.0.1 (HAProxy on port 80)

Stop: `docker compose down`

---

## 2. Run on Minikube (HAProxy)

```bash
minikube start --driver=docker
# Build images
docker build -t ttruc09/public-notes-mongo:latest -f mongo/Dockerfile ./mongo
docker build -t ttruc09/public-notes-app1:latest -f app/Dockerfile .
docker build -t ttruc09/public-notes-haproxy:latest -f haproxy/Dockerfile ./haproxy
# Load to minikube
minikube image load ttruc09/public-notes-mongo:latest
minikube image load ttruc09/public-notes-app1:latest
minikube image load ttruc09/public-notes-haproxy:latest
# Deploy
kubectl apply -f kubernetes-deployments/
# Get URL
minikube service haproxy-service --url
```

---

## 3. Run on Minikube (Ingress)

```bash
minikube addons enable ingress
# Remove HAProxy if deployed
kubectl delete deployment haproxy-deployment 2>/dev/null; kubectl delete service haproxy-service 2>/dev/null; kubectl delete configmap haproxy-config 2>/dev/null
kubectl apply -f kubernetes-deployments/ingress.yaml
# Add hosts entry (Windows: C:\Windows\System32\drivers\etc\hosts)
#   With minikube tunnel (Windows/macOS Docker driver):  127.0.0.1   ttrinh.notes.com
#   Without tunnel (Linux, route works):                 <minikube-ip> ttrinh.notes.com
minikube tunnel  # keep terminal open
```
Visit: http://ttrinh.notes.com  (HTTP only — no HTTPS)

---

## Troubleshooting

### Issue: `https://ttrinh.notes.com` / browser cannot open the site

Two common causes:
1. **Using `https://`** — the app serves **HTTP only** (port 80, no TLS). Always use `http://ttrinh.notes.com`.
2. **Hosts file points to the Minikube IP** (e.g. `192.168.49.2`). On Windows/macOS with the **Docker driver** that IP is not routable from the host. Point it to `127.0.0.1` and run `minikube tunnel`.

Fix (Windows):
```powershell
# 1. Make sure the tunnel is running (in a separate terminal, keep it open)
minikube tunnel

# 2. Edit hosts with admin rights: C:\Windows\System32\drivers\etc\hosts
#    Use 127.0.0.1 (NOT the minikube ip) when using the tunnel:
#    127.0.0.1 ttrinh.notes.com

# 3. Flush DNS
ipconfig /flushdns
```
Then open `http://ttrinh.notes.com` (http, not https).

Verify:
```bash
kubectl get ingress                 # ADDRESS should be set
kubectl get svc -n ingress-nginx    # controller port 80 mapped
```

### Issue: Cannot access app via Minikube IP directly

If `http://<MINIKUBE_IP>` does not load, use the tunnel + `127.0.0.1` hosts entry as above, or reach it with a Host header through the tunnel.

---

If Ingress still fails: `minikube addons disable ingress; minikube addons enable ingress; kubectl delete -f kubernetes-deployments/; kubectl apply -f kubernetes-deployments/`

### Issue: Mongo ExitCode 14 / restart loop

MongoDB cannot write to `./mongo-data`.
- Ensure folder exists (`mkdir mongo-data`).
- Permissions: Linux `sudo chown -R 999:999 ./mongo-data`; Windows/macOS: add folder to Docker Desktop → Settings → Resources → File Sharing.

### Alternative: Named volume (avoid permission issues)

Replace bind mount in `docker-compose.yml`:
```yaml
volumes:
  - mongo-data:/data/db
volumes:
  mongo-data:
```

### HAProxy DNS on Linux (EC2)

If HAProxy can't resolve backends, use app port `5000` in `haproxy.cfg`:
```yaml
backend flask_backends
    balance roundrobin
    server app1 app1:5000 check
    server app2 app2:5000 check
```
`app.run(host="0.0.0.0", port=5000)` is already set. Rebuild: `docker compose up -d --build haproxy`.

### Full reset (if stuck)

```bash
docker compose down -v --remove-orphans
docker system prune -f --volumes
docker compose build --no-cache
docker compose up -d
```


---


## Cleanup

```bash
kubectl delete -f kubernetes-deployments/  # K8s
docker compose down                        # Docker Compose
```

---


