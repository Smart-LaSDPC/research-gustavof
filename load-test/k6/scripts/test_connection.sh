#!/bin/bash

# Garante que estamos no diretório correto
cd "$(dirname "$0")"

# Carrega as configurações
if [ ! -f "./config.sh" ]; then
    echo "Erro: config.sh não encontrado"
    exit 1
fi
source ./config.sh

echo "Iniciando testes de conexão..."
echo "Host: $BASE_HOST"
echo "Usuário: $USERNAME"
echo "Portas: ${PORTS[*]}"
echo

falhas=0
for port in "${PORTS[@]}"; do
    echo -n "Testando conexão na porta $port... "
    if ssh -p "$port" "$USERNAME@$BASE_HOST" "echo 'Conexão OK'" &> /dev/null; then
        echo "OK"
    else
        echo "FALHOU"
        echo "Verifique as configurações de SSH para a porta $port"
        ((falhas++))
    fi
done

echo
if [ $falhas -eq 0 ]; then
    echo "Todos os testes de conexão foram bem-sucedidos!"
    exit 0
else
    echo "ATENÇÃO: $falhas conexões falharam"
    exit 1
fi