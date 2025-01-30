#!/bin/bash
set -e

# Add kubectl aliases
echo "alias kubectl='microk8s kubectl'" >> ~/.bashrc
echo "alias k='microk8s kubectl'" >> ~/.bashrc

# Install microk8s
echo "Installing MicroK8s..."
sudo snap install microk8s --classic --channel=1.32

# Wait for microk8s to be ready
echo "Waiting for MicroK8s to be ready..."
microk8s status --wait-ready

# Check nodes
microk8s kubectl get nodes

# Setup kubectl config
mkdir -p ~/.kube
microk8s config > "$HOME/.kube/config"
chmod 0600 ~/.kube/config

# Setup permissions
sudo usermod -a -G microk8s "$USER"
chmod 0700 ~/.kube

echo "Installation complete! Please log out and log back in for changes to take effect."
