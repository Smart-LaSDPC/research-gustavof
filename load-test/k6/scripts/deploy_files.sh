#!/bin/bash

# Garante que estamos no diretório correto
cd "$(dirname "$0")"

# Carrega as configurações
if [ ! -f "./config.sh" ]; then
    echo "Erro: config.sh não encontrado"
    exit 1
fi
source ./config.sh

# Função para fazer deploy dos arquivos em uma VM
deploy_vm() {
    local port=$1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando deploy na VM $port"
    
    # Criar estrutura de diretórios na VM
    ssh -i ~/.ssh/id_andromeda -p "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br" "mkdir -p \
        $REMOTE_DIR/iot/results/logs \
        $REMOTE_DIR/iot/results/graphs \
        $REMOTE_DIR/pipeline/results/logs \
        $REMOTE_DIR/pipeline/results/graphs"
    
    # Copiar arquivos de teste
    scp -i ~/.ssh/id_andromeda -P "$port" "../iot/iot_test.js" "$USERNAME@andromeda.lasdpc.icmc.usp.br:$REMOTE_DIR/iot/"
    scp -i ~/.ssh/id_andromeda -P "$port" "../pipeline/load_test_pipeline.js" "$USERNAME@andromeda.lasdpc.icmc.usp.br:$REMOTE_DIR/pipeline/"
    
    # Copiar scripts de análise específicos para cada diretório
    scp -i ~/.ssh/id_andromeda -P "$port" "../iot/analyze_results.py" "$USERNAME@andromeda.lasdpc.icmc.usp.br:$REMOTE_DIR/iot/"
    scp -i ~/.ssh/id_andromeda -P "$port" "../pipeline/analyze_results.py" "$USERNAME@andromeda.lasdpc.icmc.usp.br:$REMOTE_DIR/pipeline/"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deploy concluído na VM $port"
}

echo "Iniciando deploy em todas as VMs"

# Deploy em todas as VMs simultaneamente
for port in "${PORTS[@]}"; do
    deploy_vm "$port" &
done

# Aguarda conclusão de todos os deploys
wait

echo "Deploy concluído em todas as VMs!"