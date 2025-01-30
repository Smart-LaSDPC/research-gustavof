# Database

## CloudNativePG   [text](https://cloudnative-pg.io/)helm repo add cnpg https://cloudnative-pg.github.io/charts -n usp-dev
helm install cnpg-controller cnpg/cloudnative-pg -n usp-dev


### Zalando postgres operato [text](https://github.com/zalando/postgres-operator/blob/master/docs/quickstart.md#deployment-options)

# add repo for postgres-operator
helm repo add postgres-operator-charts https://opensource.zalando.com/postgres-operator/charts/postgres-operator

# install the postgres-operator
helm install postgres-operator postgres-operator-charts/postgres-operator -n usp-dev

helm upgrade postgres-operator postgres-operator-charts/postgres-operator -n usp-dev

# add repo for postgres-operator-ui
helm repo add postgres-operator-ui-charts https://opensource.zalando.com/postgres-operator/charts/postgres-operator-ui

# install the postgres-operator-ui
helm install postgres-operator-ui postgres-operator-ui-charts/postgres-operator-ui -n usp-dev

kubectl get pod -l name=postgres-operator
kubectl logs "$(kubectl get pod -l name=postgres-operator --output='name')"


### fix calico
kubectl apply -f calico-rbac.yaml
kubectl delete pod -n kube-system -l k8s-app=calico-node


## Creating the cluster
- k apply -f cluster-manifest.yml -n usp-dev


## Connect to the database

# Use the master for DDL (CREATE, ALTER, DROP)
k port-forward svc/pg-cluster-pooler 5432:5432 -n usp-dev

username: kubectl get secret usp.pg-cluster.credentials.postgresql.acid.zalan.do -n usp-dev -o jsonpath='{.data.username}' | base64 -d
password: kubectl get secret usp.pg-cluster.credentials.postgresql.acid.zalan.do -n usp-dev -o jsonpath='{.data.password}' | base64 -d
e.g
username: usp
password: 0puJtnX8hSon7DsRsYQz0rbICL0OyX2guC0mRGZolHhuzZf3AuaQFitSh7DYQHUD

# Use the pooler for queries or DML (SELECT, INSERT, UPDATE, DELETE) - and to connect the apps to it
username: kubectl get secret pooler.pg-cluster.credentials.postgresql.acid.zalan.do -n usp-dev -o jsonpath='{.data.username}' | base64 -d
password: kubectl get secret pooler.pg-cluster.credentials.postgresql.acid.zalan.do -n usp-dev -o jsonpath='{.data.password}' | base64 -d
e.g
username: pooler
password: 3mjcGq43XTcSGq39qxqmyNJYxDXAQWesaVHBdJhTvQIbMcZ9BsIQ3lYqa5g99KFt

[IMPORTANT]
To allow pooler to access the ac_sensor table, you need to grant the necessary privileges. Here are the steps to do this:

GRANT ALL PRIVILEGES ON TABLE ac_sensor TO pooler;
-- If you're using SERIAL for the id column, you'll also need to grant permissions on the sequence
GRANT USAGE, SELECT ON SEQUENCE ac_sensor_id_seq TO pooler;

## Cleanup Database Cluster
To completely remove the database cluster and all associated resources, run these commands in order:

# Delete the cluster
kubectl delete -f cluster-manifest.yml -n usp-dev

# Delete associated PVCs
kubectl delete pvc pgdata-pg-cluster-0 -n usp-dev
kubectl delete pvc pgdata-pg-cluster-1 -n usp-dev
kubectl delete pvc pgdata-pg-cluster-2 -n usp-dev
kubectl delete pvc postgres-pvc -n usp-dev

# Delete any remaining resources
kubectl delete postgresql pg-cluster -n usp-dev
kubectl delete svc pg-cluster -n usp-dev
kubectl delete svc pg-cluster-pooler -n usp-dev
kubectl delete endpoints pg-cluster -n usp-dev
kubectl delete endpoints pg-cluster-pooler -n usp-dev

# Delete PodDisruptionBudget
kubectl delete pdb postgres-pg-cluster-pdb -n usp-dev

# Optional: If you want to delete all related resources in one command (use with caution)
kubectl get pods -n usp-dev --show-labels | grep pg-cluster


kubectl delete all,secrets,configmaps,endpoints,pvc,pdb -l application=spilo -n usp-dev

# If still having issues, force delete the PostgreSQL custom resource
kubectl patch postgresql pg-cluster -n usp-dev -p '{"metadata":{"finalizers":null}}' --type=merge
kubectl delete postgresql pg-cluster -n usp-dev --force --grace-period=0
