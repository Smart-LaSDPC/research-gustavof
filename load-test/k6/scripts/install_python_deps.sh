#!/bin/bash

# Garante que estamos no diretório correto
cd "$(dirname "$0")"

# Carrega as configurações
if [ ! -f "./config.sh" ]; then
    echo "Erro: config.sh não encontrado"
    exit 1
fi
source ./config.sh

# Função para instalar Python e dependências em uma VM
install_python_deps_vm() {
    local port=$1
    echo "Instalando Python e dependências na VM porta $port..."
    
    # Comandos para instalar Python e dependências
    ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_andromeda -p "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br" "
        # Atualiza os pacotes
        sudo apt-get update &&
        
        # Instala Python e dependências via apt
        sudo apt-get install -y \
            python3 \
            python3-pandas \
            python3-matplotlib \
            python3-seaborn \
            python3-dateutil &&
        
        # Verifica a instalação do Python
        python3 --version &&
        
        # Verifica se os módulos podem ser importados
        python3 -c 'import pandas; import matplotlib; import seaborn; import dateutil'
    "
    
    if [ $? -eq 0 ]; then
        echo "Python e dependências instalados com sucesso na VM porta $port"
        return 0
    else
        echo "ERRO: Falha ao instalar Python e dependências na VM porta $port"
        return 1
    fi
}

# Instala em todas as VMs
falhas=0
for port in "${PORTS[@]}"; do
    echo "----------------------------------------"
    echo "Iniciando instalação na porta $port"
    echo "----------------------------------------"
    
    if install_python_deps_vm "$port"; then
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
    echo "Python e dependências instalados com sucesso em todas as VMs!"
    exit 0
else
    echo "ATENÇÃO: Houve falhas em algumas instalações"
    exit 1
fi 