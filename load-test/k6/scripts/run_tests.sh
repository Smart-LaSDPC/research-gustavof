#!/bin/bash
# bash run_tests.sh -t iot
# Without analysis: bash run_tests.sh -t iot
# With analysis: bash run_tests.sh -t iot -a

# Garante que estamos no diretório correto
cd "$(dirname "$0")"

# Carrega as configurações
if [ ! -f "./config.sh" ]; then
    echo "Erro: config.sh não encontrado"
    exit 1
fi
source ./config.sh

# Contador de falhas
falhas=0

# Função para executar testes em uma VM
run_test_vm() {
    local port=$1
    local test_type=$2
    local run_analysis=$3
    local test_dir=""
    local test_file=""
    local analyze_script=""
    
    # Define o diretório, arquivo e script de análise baseado no tipo
    case $test_type in
        "iot")
            test_dir="iot"
            test_file="iot_test.js"
            analyze_script="../iot/analyze_results.py"
            ;;
        "pipeline")
            test_dir="pipeline"
            test_file="load_test_pipeline.js"
            analyze_script="../pipeline/analyze_results.py"
            ;;
    esac
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando teste $test_type na VM $port"
    
    # Executar o teste e análise
    if ! ssh -i ~/.ssh/id_andromeda -p "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br" "cd $REMOTE_DIR/$test_dir && \
        bash run_pipeline.sh \
        -e VM_PORT=$port \
        -e VM_NAME=vm${port} \
        $([ "$run_analysis" = true ] && echo "&& python3 analyze_results.py $port $test_type")"; then
        ((falhas++))
    fi

    # Copia os resultados apenas se a análise estiver ativada
    if [ "$run_analysis" = true ]; then
        echo "Copiando resultados da VM $port"
        
        # Cria diretórios locais se não existirem
        mkdir -p "../$test_dir/results/logs"
        mkdir -p "../$test_dir/results/graphs"
        
        # Copia os arquivos com identificador da VM
        scp -i ~/.ssh/id_andromeda -P "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br:$REMOTE_DIR/$test_dir/results/logs/${test_type}_test_vm${port}_results.json" "../$test_dir/results/logs/" || true
        scp -i ~/.ssh/id_andromeda -P "$port" "$USERNAME@andromeda.lasdpc.icmc.usp.br:$REMOTE_DIR/$test_dir/results/graphs/${test_type}_test_vm${port}_metrics.png" "../$test_dir/results/graphs/" || true
    fi
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Finalizando teste $test_type na VM $port"
}

# Função de ajuda
show_help() {
    echo "Uso: $0 [opções]"
    echo "Opções:"
    echo "  -t, --type     Tipo de teste (iot ou pipeline)"
    echo "  -a, --analyze  Executa análise após o teste (opcional)"
    echo "  -h, --help     Mostra esta ajuda"
    echo
    echo "Exemplos:"
    echo "  $0 -t iot              # Executa apenas teste IoT"
    echo "  $0 -t pipeline -a      # Executa teste Pipeline com análise"
}

# Parse dos argumentos
TEST_TYPE=""
RUN_ANALYSIS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            TEST_TYPE="$2"
            shift 2
            ;;
        -a|--analyze)
            RUN_ANALYSIS=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Opção inválida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validação do tipo de teste
if [[ ! "$TEST_TYPE" =~ ^(iot|pipeline)$ ]]; then
    echo "Erro: Tipo de teste inválido. Use 'iot' ou 'pipeline'"
    show_help
    exit 1
fi

echo "Iniciando teste $TEST_TYPE em todas as VMs"

# Executa o teste em todas as VMs simultaneamente
for port in "${PORTS[@]}"; do
    run_test_vm "$port" "$TEST_TYPE" "$RUN_ANALYSIS" &
done

# Aguarda a conclusão de todas as VMs
wait

# Relatório final
echo "----------------------------------------"
echo "Relatório de execução dos testes $TEST_TYPE:"
echo "Total de VMs: ${#PORTS[@]}"
echo "Sucessos: $((${#PORTS[@]} - falhas))"
echo "Falhas: $falhas"
echo "----------------------------------------"

if [ "$falhas" -eq 0 ]; then
    echo "Testes $TEST_TYPE concluídos com sucesso em todas as VMs!"
    echo "Resultados disponíveis em:"
    echo "- Logs: ../$TEST_TYPE/results/logs/"
    echo "- Gráficos: ../$TEST_TYPE/results/graphs/"
    exit 0
else
    echo "ATENÇÃO: Houve falhas em algumas execuções dos testes $TEST_TYPE"
    exit 1
fi