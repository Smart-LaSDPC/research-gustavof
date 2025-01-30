import subprocess
from src.config import config

## TODO: Consider using the official Kubernetes Python client instead


# Function to get ingress details using `kubectl describe ingress`
def get_ingress_details(ingress_name, namespace):
    try:
        # Check if microk8s is available when config.MICRO_K8S is True
        if config.MICRO_K8S:
            try:
                subprocess.run(["microk8s", "--version"], capture_output=True, check=True)
                cmd = ["microk8s", "kubectl"]
            except (subprocess.CalledProcessError, FileNotFoundError):
                return "Error: microk8s is not installed or not in PATH"
        else:
            cmd = ["kubectl"]
            
        cmd.extend(["describe", "ingress", ingress_name, "-n", namespace])
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error fetching ingress details: {e.stderr.strip()}"

# Function to parse ingress details
def parse_ingress_details(raw_output):
    details = {
        "Name": None,
        "Namespace": None,
        "Host": None,
        "Load Balancer Type": None,
        "Ingress Class": None,
    }

    for line in raw_output.splitlines():
        line = line.strip()
        if line.startswith("Name:"):
            details["Name"] = line.split(":", 1)[1].strip()
        elif line.startswith("Namespace:"):
            details["Namespace"] = line.split(":", 1)[1].strip()
        elif "Host" in line and "Path" in line:  # Start of rules section
            details["Host"] = line.split(" ")[0].strip()
        elif "nginx.ingress.kubernetes.io/load-balance" in line:
            details["Load Balancer Type"] = line.split(":", 1)[1].strip()
        elif "Ingress Class:" in line:  # Changed from IngressClass: to match actual output
            details["Ingress Class"] = line.split(":", 1)[1].strip()
    
    return details


def update_ingress_load_balancer(ingress_name, namespace, load_balancer_type):
    """
    Updates the load balancer type annotation for a Kubernetes ingress
    Valid load_balancer_type values: 'round_robin', 'least_conn', 'ip_hash'
    """
    try:
        # Check if microk8s is available when config.MICRO_K8S is True
        if config.MICRO_K8S:
            try:
                subprocess.run(["microk8s", "--version"], capture_output=True, check=True)
                cmd = ["microk8s", "kubectl"]
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False, "Error: microk8s is not installed or not in PATH"
        else:
            cmd = ["kubectl"]
            
        annotation = f"nginx.ingress.kubernetes.io/load-balance={load_balancer_type}"
        cmd.extend(["annotate", "ingress", ingress_name, 
                   f"{annotation}", "--overwrite", "-n", namespace])
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error updating ingress load balancer: {e.stderr.strip()}"
