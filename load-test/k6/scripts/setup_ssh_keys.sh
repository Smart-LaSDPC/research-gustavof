#!/bin/bash

# Garante que estamos no diretório correto
cd "$(dirname "$0")"

# Carrega as configurações
if [ ! -f "./config.sh" ]; then
    echo "Erro: config.sh não encontrado"
    exit 1
fi
source ./config.sh

# Função para copiar a chave pública para cada porta
setup_ssh_key() {
    local port=$1
    echo "Configurando acesso SSH para porta $port..."
    
    # Tenta copiar a chave
    if ! ssh-copy-id -p "$port" "$USERNAME@$BASE_HOST"; then
        echo "ERRO: Falha ao copiar chave SSH para porta $port"
        return 1
    fi
    
    # Testa a conexão
    if ! ssh -p "$port" "$USERNAME@$BASE_HOST" "echo 'Teste OK'" &> /dev/null; then
        echo "ERRO: Falha ao testar conexão na porta $port"
        return 1
    fi
    
    return 0
}

# Verifica se já existe uma chave SSH
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "Gerando novo par de chaves SSH..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" || {
        echo "ERRO: Falha ao gerar chaves SSH"
        exit 1
    }
fi

# Configura para todas as portas
echo "Configurando chaves SSH para todas as portas..."
for port in "${PORTS[@]}"; do
    if setup_ssh_key "$port"; then
        echo "Configuração da porta $port concluída com sucesso"
    else
        echo "ERRO: Falha na configuração da porta $port"
    fi
done

echo "Configuração das chaves SSH concluída!"