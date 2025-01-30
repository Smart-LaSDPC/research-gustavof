# Distributed Software Architecture (DSA)

## Overview
This repository contains the codebase for the Distributed Software Architecture (DSA) designed for scalable applications, as proposed in the accompanying paper. The DSA is based on the principles of the Reactive Manifesto (RM) and aims to optimize distributed processing, latency, flexibility, security, cost-effectiveness, and scalability within smart building environments.

## Features
- Implementation of the DSA architecture following RM principles.
- Analysis of different deployment configurations, with a focus on container orchestrators.
- Performance testing demonstrating the benefits of using a container orchestrator, including enhanced distributed processing, reduced latency, increased flexibility, improved security, and cost-effectiveness.
- Application of the Design Science Research (DSR) methodology to iteratively develop and refine the DSA artifact.
- Testing procedures emphasizing performance as the primary evaluation metric.
- Integration with Multi-Agent Systems
- Extensive applicability across various domains, including Smart Home setups, Campus environments, City infrastructure, and Health-related applications.

## Infrastructure Components

### Kubernetes Cluster (MicroK8s)
- Lightweight Kubernetes distribution with essential add-ons:
  - DNS for service discovery
  - Observability stack (Prometheus, Grafana, Kibana, FluentD, ElasticSearch, Logstash, Loki)
- System optimization through automated scripts for:
  - Increased file descriptors
  - Optimized TCP settings
  - Enhanced network performance

### Database Layer
- PostgreSQL deployment options:
  1. Simple deployment with basic PostgreSQL instance and Prometheus exporter
  2. Advanced cluster using Zalando Operator with:
     - High availability (N nodes)
     - Connection pooling (pgbouncer)
     - Automated failover
     - Resource management
     - Custom extensions (UI)

### Monitoring & Observability
- Comprehensive stack with:
  - Prometheus for metrics collection
  - Grafana for visualization
  - Custom dashboards for PostgreSQL, NGINX, and system metrics
  - Kibana for log analysis
  - Loki for log storage
  - FluentD for log collection
  - ElasticSearch for log indexing
  - Logstash for log processing
- Automated metric collection via ServiceMonitor
- Secure metric collection through network policies

### AI Service Layer
- Machine Learning service for cluster log data processing:
  - Custom AI Agent framework to support cluster intelligence
  - Uses Langchain and LLMs to process the data and generate suggestions for decision (detects anomalies, load balancing, etc)
  - UI developed with Streamlit
  - Rate limiting and request validation

### API Service Layer
- RESTful API built with Go (Gin framework):
  - High-performance request handling
  - Middleware support for authentication and logging
  - Structured error handling and validation
- Key endpoints:
  - IoT data ingestion and processing
  - Device management and configuration


## Load Testing Framework

### K6 Testing Suite
- Multiple distribution patterns:
  - Normal, Poisson, Uniform, and Exponential distributions
- Configurable and extensible parameters:
  - Virtual Users: 50-5000
  - Test durations: 5m-15m
  - Custom wait time distributions
- Pipeline-based execution and automated results processing

## Requirements
- Container orchestrator (MicroK8s or compatible Kubernetes distribution)
- Helm 3
- Programming languages: 
  - Go for API service
  - Python for AI service
- Database: PostgreSQL
- Monitoring tools: Prometheus, Grafana, Kibana, FluentD, ElasticSearch, Logstash, Loki
- Load testing: K6
- ML frameworks: Langchain


## Contribution
We welcome contributions to enhance the functionality, performance, and usability of the DSA codebase. If you're interested in contributing, please follow these guidelines:
- Fork the repository and create a new branch for your feature or bug fix.
- Ensure that your code adheres to the established coding standards and practices.
- Submit a pull request detailing the changes made and any relevant documentation updates.
- Participate in code reviews and discussions to facilitate collaborative development.

## License
MIT License 

## Acknowledgments
This research and development effort were made possible by the contributions of Gustavo Freire, Joao Gabriel Zanao, Herminio Paucar e Julio Cezar Estrella and the support of the Laboratory of Distributed Systems and Concurrent Programming (LaSDPC) at São Paulo University.