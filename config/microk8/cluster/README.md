# MicroK8s Setup and Configuration

## Cluster Setup

Reference: [MicroK8s](https://microk8s.io/docs/getting-started)

# Install the master node:
```bash
   bash install_master.sh
```
# Install the worker nodes:
1. Go to master node and run:
```bash
microk8s add-node
```
Then copy the token and run in the worker node:
```bash
microk8s join <token>
```
Repeat the process for all worker nodes.

# [Optional] Label the cluster nodes
# Label the control-plane node
```bash
    kubectl label node <VMhostname-VMinstance> node-role.kubernetes.io/control-plane=true
    e.g
    kubectl label node and02-vm1 node-role.kubernetes.io/control-plane=true

```
# Label the worker nodes
```bash
    kubectl label node <VMhostname-VMinstance> node-role.kubernetes.io/worker=true
    e.g
    kubectl label node and01-vm1 node-role.kubernetes.io/worker=true
    kubectl label node and02-vm2 node-role.kubernetes.io/worker=true
    kubectl label node and03-vm1 node-role.kubernetes.io/worker=true
    kubectl label node and03-vm2 node-role.kubernetes.io/worker=true

```
## Storage and DNS

# Install hostpath-storage
1. Enable the DNS addon:
   ```bash
   microk8s enable hostpath-storage
   ```

## DNS Configuration

1. Enable the DNS addon:
   ```bash
   microk8s enable dns
   ```

## Certificate Configuration

1. Edit the certificate configuration template:
   ```bash
   sudo vim /var/snap/microk8s/current/certs/csr.conf.template
   ```

2. Add the following DNS and IP entries to the configuration file:
   ```conf
   DNS.6 = andromeda.lasdpc.icmc.usp.br
   IP.6 = 10.1.1.21    # Note: Change with instance IP and update the DNS entry in the DNS server
   ```

3. Refresh the certificates by running these commands in order:
   ```bash
   sudo microk8s refresh-certs --cert server.crt
   sudo microk8s refresh-certs --cert ca.crt
   sudo microk8s refresh-certs --cert front-proxy-client.crt
   ```
> **Note**: After refreshing certificates, MicroK8s services will restart automatically.

## Verification

To verify the configuration:
1. Check DNS resolution:
   ```bash
   kubectl get pods -n kube-system | grep dns
   ```

2. Verify the certificates:
   ```bash
   microk8s status
   ```

