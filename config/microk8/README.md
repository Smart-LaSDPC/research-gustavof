# MicroK8s Setup and Configuration

## Initial Setup

1. Install and configure MicroK8s following the official documentation:
   https://microk8s.io/docs/getting-started

2. Export the kubeconfig file:
   ```bash
   microk8s config > config
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
   IP.6 = 10.1.1.21    # Note: Use the next available IP.x number
   ```

3. Refresh the certificates by running these commands in order:
   ```bash
   sudo microk8s refresh-certs              # Refresh all certificates
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


   Observability has been enabled (user/pass: admin/prom-operator)

