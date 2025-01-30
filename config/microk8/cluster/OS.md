# Operating System Tuning

To optimize your system for running MicroK8s, execute the following command to adjust OS limits and kernel parameters:

```bash
sudo bash tune-os-limits.sh
```

This script will:
- Increase maximum file descriptors
- Adjust kernel parameters for networking
- Configure system limits for optimal container performance

Run this command before starting your MicroK8s cluster to ensure proper system configuration.