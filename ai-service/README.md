## Steps to run

1. Create a virtual environment
```bash
python3 -m venv venv    
source venv/bin/activate
```

2. Install the dependencies
```bash
make install 
or 
pip install -r requirements.txt
```

3. Run the streamlit app
```bash
make run
or 
streamlit run main.py --server.port 6321
```

4. Preparing the cluster test cases (each on a separate terminal)
```bash
sudo kubectl port-forward svc/ingress-nginx-controller -n ingress-nginx 80:80
sudo kubectl port-forward svc/prometheus-operated -n monitoring 9090:9090
or 
sudo microk8s kubectl port-forward svc/prometheus-operated -n observability 9090:9090
sudo microk8s kubectl port-forward svc/kube-prom-stack-grafana -n observability 3000:3121
k logs svc/ingress-nginx-controller -n ingress-nginx -f
k6 run load_simple_test.js
```