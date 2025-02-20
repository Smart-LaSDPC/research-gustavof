### NGINX Ingress Controller
### Install Ingress
- helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
- helm repo update
- helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace -f values.yaml

- helm show values ingress-nginx/ingress-nginx | less
- helm get values ingress-nginx --namespace ingress-nginx
- kubectl get svc -n ingress-nginx

## Uninstall
- helm uninstall ingress-nginx --namespace ingress-nginx 

## Test Ingress 
- sudo kubectl port-forward svc/ingress-nginx-controller -n ingress-nginx 80:80
- sudo microk8s kubectl port-forward svc/ingress-nginx-controller -n ingress-nginx 80:80
- curl -v -H "Host: iot-api.local" http://localhost:80/

# [optional] Update /etc/hosts to point local to ingress-nginx-controller
- /etc/hosts is Configured
- 127.0.0.1 iot-api.local
- http://iot-api.local/

## Service Monitor
1. Identify the Proper Labels for ServiceMonitor (search for matchLabels)
- kubectl get prometheus -n observability -o yaml
- kubectl get servicemonitor -n observability --show-labels
- kubectl get endpoints -n observability

2. Create the ServiceMonitor

- kubectl apply -f ingress-nginx-servicemonitor.yaml --namespace=observability
- kubectl get servicemonitor nginx-ingress-controller-metrics -n observability -o yaml
3. Delete the ServiceMonitor
- kubectl delete servicemonitor ingress-nginx-controller-metrics -n observability


### HPA
- kubectl get hpa -n ingress-nginx
- kubectl describe hpa ingress-nginx-controller -n ingress-nginx
Remember to have the metrics server installed in your cluster for the HPA to work. If you need to install it:
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
``` 

### Test Ingress
curl -v -H "Host: iot-api.local" http://<CONTROL_PLANE_IP>/
curl -v -H "Host: iot-api.local" http://  


### Debugging
kubectl get prometheus -n observability
kubectl describe prometheus kube-prom-stack-kube-prome-prometheus -n observability
kubectl get servicemonitor -n observability
kubectl get endpoints -n observability
kubectl get ing -A

## Checking the load balancer 
kubectl get configmap -n ingress-nginx ingress-nginx-controller -o yaml
 