Install the observaibility stack

1. Enable the DNS addon:
   ```bash
   microk8s enable observability
   ```


sudo kubectl port-forward svc/prometheus-operated -n monitoring 9090:9090
sudo kubectl port-forward svc/kube-prom-stack-grafana -n monitoring 3000:3000


sudo microk8s kubectl port-forward svc/prometheus-operated -n observability 9090:9090
sudo microk8s kubectl port-forward svc/kube-prom-stack-grafana -n observability 3121:80
