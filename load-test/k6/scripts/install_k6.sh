#!/bin/bash

# Garante que estamos no diretório correto
cd "$(dirname "$0")"

# Carrega as configurações
if [ ! -f "./config.sh" ]; then
    echo "Erro: config.sh não encontrado"
    exit 1
fi
source ./config.sh

# Função para instalar k6 em uma VM
install_k6_vm() {
    local port=$1
    echo "Instalando k6 na VM porta $port..."
    
    # First ensure NOPASSWD sudo access
    ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_andromeda -p "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br" "echo '$USERNAME ALL=(ALL) NOPASSWD: ALL' | sudo tee /etc/sudoers.d/k6_install" &&
    
    # Then install k6
    ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_andromeda -p "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br" "
        sudo snap install k6 &&
        k6 version
    "
    
    if [ $? -eq 0 ]; then
        echo "k6 instalado com sucesso na VM porta $port"
        return 0
    else
        echo "ERRO: Falha ao instalar k6 na VM porta $port"
        return 1
    fi
}

# Instala k6 em todas as VMs
falhas=0
for port in "${PORTS[@]}"; do
    echo "----------------------------------------"
    echo "Iniciando instalação na porta $port"
    echo "----------------------------------------"
    
    if install_k6_vm "$port"; then
        echo "✓ VM porta $port configurada com sucesso"
    else
        echo "✗ Falha na VM porta $port"
        ((falhas++))
    fi
    echo
done

# Relatório final
echo "----------------------------------------"
echo "Relatório de instalação:"
echo "Total de VMs: ${#PORTS[@]}"
echo "Sucessos: $((${#PORTS[@]} - falhas))"
echo "Falhas: $falhas"
echo "----------------------------------------"

if [ $falhas -eq 0 ]; then
    echo "k6 instalado com sucesso em todas as VMs!"
    exit 0
else
    echo "ATENÇÃO: Houve falhas em algumas instalações"
    exit 1
fi