# Configuration Directory Structure

## Overview
This directory contains Kubernetes and MicroK8s configuration files organized by functionality. The main sections are:

### 1. MicroK8s Cluster Setup (`/microk8/cluster/`)
- Basic cluster configuration and setup scripts
- Operating system tuning for optimal performance
- Installation scripts for master and worker nodes
- Certificate management

Key files:
- `install_master.sh` - Master node installation script
- `tune-os-limits.sh` - System optimization script
- `OS.md` - Operating system tuning documentation

### 2. Infrastructure (`/microk8/infra/`)
Contains configurations for core infrastructure components:

#### a. Database (`/infra/database/`)
- PostgreSQL cluster configurations
- Simple standalone PostgreSQL setup
- Database monitoring and metrics exporters

Two deployment options:
- `cluster/` - High-availability PostgreSQL cluster using Zalando operator
- `simple/` - Single instance PostgreSQL deployment

#### b. Ingress (`/infra/ingress/`)
- NGINX Ingress Controller configuration
- Custom resource definitions
- Load balancing settings
- SSL/TLS configurations

#### c. Observability (`/infra/observability/`)
- Monitoring stack configuration
- Grafana dashboards for:
  - PostgreSQL metrics
  - NGINX Ingress metrics
  - Pod metrics and resource usage
- Service monitors for Prometheus

### 3. Microservices (`/microk8/microservices/`)
Contains Kubernetes configurations for application services:

#### a. API Service (`/microservices/api/`)
- Main IoT application deployment configurations
- Includes:
  - `deployment.yml` - IoT application deployment with 8 replicas
  - `hpa.yml` - Horizontal Pod Autoscaler (8-36 replicas)
  - `service.yml` - Service configuration for port 8080
  - `secret.yml` - ConfigMaps and Secrets for environment variables

Key features:
- Node affinity rules to avoid control-plane nodes
- Pod anti-affinity for zone-level spreading
- Topology spread constraints for high availability
- Resource limits and requests defined
- PostgreSQL cluster integration