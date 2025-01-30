#!/bin/bash
# This script optimizes system network and file descriptor limits to handle high load scenarios
# and prevent "connection reset by peer" errors. The improvements include:
#
# 1. Ephemeral Port Range: Changed from 32768-60999 (28,231 ports) to 1024-65535 (64,511 ports)
#    - This provides more available ports for outgoing connections
#    - Helps prevent port exhaustion under high connection loads
#
# 2. TCP Backlog: Changed from 4096 to 65535
#    - Allows more pending connections in the queue
#    - Reduces connection drops during traffic spikes
#
# 3. TCP FIN Timeout: Changed from 60 to 30 seconds
#    - Frees up connections faster after they're closed
#    - Helps prevent connection resource exhaustion
#
# 4. TCP Keepalive: Changed from 7200 to 300 seconds
#    - Detects dead connections faster
#    - Frees up resources from stale connections more quickly
#
# 5. File Descriptors: Changed from 1024 to 1048576
#    - Allows many more open files and network connections
#    - Prevents "too many open files" errors under load


# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Function to check system status
check_system_status() {
    echo "=== System Limits Status ==="
    echo "Ephemeral Port Range: $(sysctl net.ipv4.ip_local_port_range | awk '{print $3,$4}')"
    echo "Max File Descriptors: $(ulimit -n)"
    echo "TCP Backlog: $(sysctl net.core.somaxconn | awk '{print $3}')"
    echo "TCP FIN Timeout: $(sysctl net.ipv4.tcp_fin_timeout | awk '{print $3}')"
    echo "TCP Keepalive Time: $(sysctl net.ipv4.tcp_keepalive_time | awk '{print $3}')"
    echo "=========================="
}

# Function to backup sysctl.conf before making changes
backup_sysctl() {
    cp /etc/sysctl.conf /etc/sysctl.conf.backup.$(date +%Y%m%d)
}

# Function to set system limits
configure_system_limits() {
    # Increase ephemeral port range
    sysctl -w net.ipv4.ip_local_port_range="1024 65535"
    echo "net.ipv4.ip_local_port_range = 1024 65535" >> /etc/sysctl.conf
    
    # Increase TCP backlog
    sysctl -w net.core.somaxconn=65535
    sysctl -w net.core.netdev_max_backlog=65535
    echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
    echo "net.core.netdev_max_backlog = 65535" >> /etc/sysctl.conf
    
    # Increase TCP timeout settings
    sysctl -w net.ipv4.tcp_fin_timeout=30
    sysctl -w net.ipv4.tcp_keepalive_time=300
    echo "net.ipv4.tcp_fin_timeout = 30" >> /etc/sysctl.conf
    echo "net.ipv4.tcp_keepalive_time = 300" >> /etc/sysctl.conf
}

# Function to increase file descriptor limits
configure_file_descriptors() {
    # Backup limits.conf
    cp /etc/security/limits.conf /etc/security/limits.conf.backup.$(date +%Y%m%d)
    
    # Add higher limits for both soft and hard file descriptors
    echo "* soft nofile 1048576" >> /etc/security/limits.conf
    echo "* hard nofile 1048576" >> /etc/security/limits.conf
    echo "root soft nofile 1048576" >> /etc/security/limits.conf
    echo "root hard nofile 1048576" >> /etc/security/limits.conf
    
    # Apply immediately for current session
    ulimit -n 1048576
}

# Function to handle system reboot
reboot_system() {
    echo "System needs to be rebooted for all changes to take full effect."
    read -p "Would you like to reboot now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Rebooting system in 5 seconds..."
        sleep 5
        reboot
    else
        echo "Please remember to reboot your system later for changes to take full effect."
    fi
}

echo "Starting OS tuning process..."

# Show current status
echo "Current system status:"
check_system_status

# Create backups
echo "Creating backups..."
backup_sysctl

# Configure system limits
echo "Configuring system limits..."
configure_system_limits

# Configure file descriptors
echo "Configuring file descriptor limits..."
configure_file_descriptors

echo "Configuration completed. New system status:"
check_system_status

# Handle reboot
reboot_system