<div align="center">

# 🛠️ kubernetescode

### CI / Source Code Repository

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)

</div>

---

This repository is the **CI half** of the TMIRT CI/CD pipeline. It contains the source code and Dockerfile for the `flaskdemo` security-testing application, and the Jenkins pipeline that builds, tests, and pushes the Docker image on every commit.

The companion CD repo is [kubernetesmanifest](../kubernetesmanifest/), which holds the Kubernetes manifests updated automatically by this pipeline and watched by ArgoCD.

---

## 🗂️ Repository Contents

| File | Purpose |
|---|---|
| 🐍 `app.py` | Deliberately vulnerable Flask web application |
| 🐳 `Dockerfile` | Container image definition (Python 3.11-slim) |
| 🔧 `Jenkinsfile` | CI pipeline: build → test → push → trigger CD |
| 📦 `requirements.txt` | Python dependencies |
| 🖼️ `templates/` | Flask HTML templates |
| 📖 `README.md` | This file |

---

## 🔄 Pipeline Overview

```
╔══════════════════════════════════╗
║     kubernetescode  (CI) ←here   ║
╚══════════════════════════════════╝
  │
  ├─ 📥  Stage: Clone repository
  ├─ 🏗️  Stage: Build image         →  tmirtdockerhub/test:<BUILD_NUMBER>
  ├─ 🧪  Stage: Test image
  ├─ 📤  Stage: Push image           →  Docker Hub
  └─ ⚡  Stage: Trigger ManifestUpdate
              │
              ▼
╔══════════════════════════════════╗
║   kubernetesmanifest  (CD)       ║
╚══════════════════════════════════╝
  │
  ├─ 🖊️  Jenkinsfile patches deployment.yaml with new image tag
  ├─ 💾  Commits & pushes to GitHub (main branch)
  └─ 🔁  ArgoCD detects the change → syncs cluster
```

### Step-by-step

1. 👨‍💻 A developer pushes code to this repo (`kubernetescode`).
2. 🏗️ Jenkins builds a Docker image tagged with the Jenkins build number.
3. 🧪 Jenkins runs a smoke test inside the container.
4. 📤 The image is pushed to Docker Hub as `tmirtdockerhub/test:<BUILD_NUMBER>`.
5. ⚡ Jenkins triggers the downstream `updatemanifest` job, passing `DOCKERTAG=<BUILD_NUMBER>`.
6. 🔁 The CD repo is patched and ArgoCD rolls out the new image to the cluster.

---

## 🔐 Application — flaskdemo

> ⚠️ **Security Notice** — This is a **deliberately vulnerable Flask web app** built for security training and penetration-testing exercises. Do not expose it to untrusted networks.

The app accepts user input via a web form and executes it as a shell command. It ships with:

| Feature | Details |
|---|---|
| 🛠️ Networking tools | `curl`, `ping`, `netcat`, `net-tools` |
| ☁️ Mock AWS credentials | Pre-baked as environment variables (`AWS_ACCESS_KEY_ID`, etc.) |
| 👤 Non-privileged user | `flaskuser` (non-login shell, restricted permissions) |
| 🌐 Exposed port | `5000` |

---

## 📜 Jenkinsfile — What It Does

The `Jenkinsfile` defines a 5-stage CI pipeline:

| Stage | Action |
|---|---|
| 📥 Clone repository | Checks out this repo via SCM |
| 🏗️ Build image | Runs `docker build` → `tmirtdockerhub/test` |
| 🧪 Test image | Runs a smoke test inside the container |
| 📤 Push image | Pushes `tmirtdockerhub/test:<BUILD_NUMBER>` to Docker Hub |
| ⚡ Trigger ManifestUpdate | Calls the `updatemanifest` downstream job with the new tag |

Required Jenkins credentials:
- `dockerhub` — credentials for `tmirtdockerhub` on Docker Hub

---

## ✅ Prerequisites

### ☁️ EC2 — Jenkins Host

Jenkins runs on an EC2 instance. Follow the [official AWS Jenkins installation guide](https://www.jenkins.io/doc/tutorials/tutorial-for-installing-jenkins-on-AWS/) *(skip the "Configure a Cloud" section for this demo)*.

Known workarounds:

> **1. `daemonize` error** during `sudo yum install jenkins java-1.8.0-openjdk-devel -y`
> → Apply the fix from [this StackOverflow answer](https://stackoverflow.com/questions/68806741/how-to-fix-yum-update-of-jenkins)

> **2. Install Docker** on EC2 after Jenkins:
> → Follow [these instructions](https://serverfault.com/questions/836198/how-to-install-docker-on-aws-ec2-instance-with-ami-ce-ee-update)

> **3. Fix Docker socket permissions:**
> ```bash
> sudo chmod 666 /var/run/docker.sock
> ```

> **4. Install Git:**
> ```bash
> sudo yum install git
> ```

### 🔌 Jenkins Plugins

Install the following plugins:

| Plugin | Purpose |
|---|---|
| 🐳 Docker Plugin | Docker build & run integration |
| 🐳 Docker Pipeline | Docker steps in `Jenkinsfile` |
| 🐙 GitHub Integration Plugin | Webhook-triggered builds |
| ⚙️ Parameterized Trigger Plugin | Pass `DOCKERTAG` to downstream job |

### 🔧 Jenkins Credentials

| ID | Type | Used For |
|---|---|---|
| `dockerhub` | Username + Password | Push image to Docker Hub |
| `github` | Username + Password/Token | CD repo — used by `updatemanifest` job |

---

## 🔁 ArgoCD Setup

Install ArgoCD in your Kubernetes cluster:

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access the ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Point ArgoCD at the [kubernetesmanifest](../kubernetesmanifest/) repo:

| Setting | Value |
|---|---|
| 🗂️ Source | `kubernetesmanifest` repo, `main` branch, path `/` |
| 🎯 Destination | Your target cluster namespace |
| 🔄 Sync Policy | Automated (auto-deploy on every commit) |

---

<div align="center">

*Built and maintained by the TMIRT team · Security Training & Research*

</div>
