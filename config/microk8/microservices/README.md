kubectl apply -f ./api -n usp-dev;

kubectl apply -f deployment.yml -n usp-dev;


kubectl get pods -o wide -n usp-dev