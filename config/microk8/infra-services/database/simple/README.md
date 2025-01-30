# Database


## Install Postgres
kubectl apply -f postgres.yml -n usp-dev

## Postgres Exporter
1. Manual approach
kubectl apply -f postgres-exporter.yml 
kubectl apply -f allow-network.yml -n observability

2. Helm approach
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install <release-name> prometheus-community/prometheus-postgres-exporter \
  --namespace <namespace> \
  --set serviceMonitor.enabled=true \
  --set serviceMonitor.namespace=observability \
  --set serviceMonitor.labels.release=kube-prom-stack \
  --set config.postgres.uri=postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@postgres:5432/<POSTGRES_DATABASE>?sslmode=disable

helm install postgres-exporter prometheus-community/prometheus-postgres-exporter \
  --namespace database \
  --set serviceMonitor.enabled=true \
  --set serviceMonitor.namespace=observability \
  --set serviceMonitor.labels.release=kube-prom-stack \
  --set config.postgres.uri=postgresql://usp:adminadminusp@postgres:5432/iot?sslmode=disable


## Service MOnitor
1. Identify the Proper Labels for ServiceMonitor (search for matchLabels)
- kubectl get prometheus -n observability -o yaml
- kubectl get servicemonitor -n observability --show-labels
- kubectl get endpoints -n observability

2. Create the ServiceMonitor
- kubectl apply -f service-monitor.yml --namespace=observability
- kubectl get servicemonitor postgres-exporter -n observability -o yaml

3. Delete the ServiceMonitor
- kubectl delete servicemonitor postgres-exporter -n observability

