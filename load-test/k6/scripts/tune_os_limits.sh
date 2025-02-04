#!/bin/bash

# Garante que estamos no diretório correto
cd "$(dirname "$0")"

# Carrega as configurações
if [ ! -f "./config.sh" ]; then
    echo "Erro: config.sh não encontrado"
    exit 1
fi
source ./config.sh

# Função para configurar os limites do SO em uma VM
tune_os_limits_vm() {
    local port=$1
    echo "Configurando limites do sistema operacional na VM porta $port..."
    
    # First ensure NOPASSWD sudo access
    ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_andromeda -p "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br" "echo '$USERNAME ALL=(ALL) NOPASSWD: ALL' | sudo tee /etc/sudoers.d/k6_install" &&
    
    ssh -i ~/.ssh/id_andromeda -p "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br" "
        # Verifica se está rodando como root
        if [ \"\$EUID\" -ne 0 ]; then 
            echo \"Executando com sudo...\"
            sudo bash -c '

                # Mostra o status atual
                echo \"=== Status dos Limites do Sistema ANTES da Configuração ===\"
                echo \"Range de Portas Efêmeras: \$(sysctl net.ipv4.ip_local_port_range | awk \"{print \\\$3,\\\$4}\")\"
                echo \"Max File Descriptors: \$(ulimit -n)\"
                echo \"TCP Backlog: \$(sysctl net.core.somaxconn | awk \"{print \\\$3}\")\"
                echo \"TCP FIN Timeout: \$(sysctl net.ipv4.tcp_fin_timeout | awk \"{print \\\$3}\")\"
                echo \"TCP Keepalive Time: \$(sysctl net.ipv4.tcp_keepalive_time | awk \"{print \\\$3}\")\"
                echo \"===================================\"

                # Aumenta o range de portas efêmeras
                sysctl -w net.ipv4.ip_local_port_range=\"1024 65535\"
                echo \"net.ipv4.ip_local_port_range = 1024 65535\" >> /etc/sysctl.conf
                
                # Aumenta o TCP backlog
                sysctl -w net.core.somaxconn=65535
                sysctl -w net.core.netdev_max_backlog=65535
                echo \"net.core.somaxconn = 65535\" >> /etc/sysctl.conf
                echo \"net.core.netdev_max_backlog = 65535\" >> /etc/sysctl.conf
                
                # Configura timeouts TCP
                sysctl -w net.ipv4.tcp_fin_timeout=30
                sysctl -w net.ipv4.tcp_keepalive_time=300
                echo \"net.ipv4.tcp_fin_timeout = 30\" >> /etc/sysctl.conf
                echo \"net.ipv4.tcp_keepalive_time = 300\" >> /etc/sysctl.conf
                
                # Configura limites de file descriptors
                cp /etc/security/limits.conf /etc/security/limits.conf.backup.\$(date +%Y%m%d) 2>/dev/null || true
                echo \"* soft nofile 1048576\" >> /etc/security/limits.conf
                echo \"* hard nofile 1048576\" >> /etc/security/limits.conf
                echo \"root soft nofile 1048576\" >> /etc/security/limits.conf
                echo \"root hard nofile 1048576\" >> /etc/security/limits.conf
                
                # Aplica os limites imediatamente
                ulimit -n 1048576
                
                # Mostra o status atual
                echo \"=== Status dos Limites do Sistema DEPOIS da Configuração ===\"
                echo \"Range de Portas Efêmeras: \$(sysctl net.ipv4.ip_local_port_range | awk \"{print \\\$3,\\\$4}\")\"
                echo \"Max File Descriptors: \$(ulimit -n)\"
                echo \"TCP Backlog: \$(sysctl net.core.somaxconn | awk \"{print \\\$3}\")\"
                echo \"TCP FIN Timeout: \$(sysctl net.ipv4.tcp_fin_timeout | awk \"{print \\\$3}\")\"
                echo \"TCP Keepalive Time: \$(sysctl net.ipv4.tcp_keepalive_time | awk \"{print \\\$3}\")\"
                echo \"===================================\"

                # Agenda o reboot para acontecer em 10 segundos
                echo \"Agendando reboot da VM em 10 segundos...\"
                nohup bash -c \"sleep 10 && reboot\" &
            '
        fi
    "
    
    if [ $? -eq 0 ]; then
        echo "Limites do SO configurados com sucesso na VM porta $port"
        echo "VM será reiniciada em 10 segundos"
        return 0
    else
        echo "ERRO: Falha ao configurar limites do SO na VM porta $port"
        return 1
    fi
}

# Configura em todas as VMs
falhas=0
for port in "${PORTS[@]}"; do
    echo "----------------------------------------"
    echo "Iniciando configuração na porta $port"
    echo "----------------------------------------"
    
    if tune_os_limits_vm "$port"; then
        echo "✓ VM porta $port configurada com sucesso"
    else
        echo "✗ Falha na VM porta $port"
        ((falhas++))
    fi
    echo
done

# Relatório final
echo "----------------------------------------"
echo "Relatório de configuração:"
echo "Total de VMs: ${#PORTS[@]}"
echo "Sucessos: $((${#PORTS[@]} - falhas))"
echo "Falhas: $falhas"
echo "----------------------------------------"

# Aguarda as VMs reiniciarem
if [ $falhas -eq 0 ]; then
    echo "Limites do SO configurados com sucesso em todas as VMs!"
    echo "Aguardando 30 segundos para as VMs reiniciarem..."
    sleep 30
    
    # Verifica se as VMs estão online novamente
    echo "Verificando conectividade com as VMs..."
    falhas_conexao=0
    for port in "${PORTS[@]}"; do
        echo -n "Testando conexão com a VM porta $port... "
        if ssh -i ~/.ssh/id_andromeda -p "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br" "echo 'OK'" &>/dev/null; then
            echo "✓ Online"
        else
            echo "✗ Offline"
            ((falhas_conexao++))
        fi
    done
    
    if [ $falhas_conexao -eq 0 ]; then
        echo "Todas as VMs reiniciaram com sucesso!"
        exit 0
    else
        echo "ATENÇÃO: $falhas_conexao VM(s) não responderam após o reboot"
        exit 1
    fi
else
    echo "ATENÇÃO: Houve falhas em algumas configurações"
    exit 1
fi 