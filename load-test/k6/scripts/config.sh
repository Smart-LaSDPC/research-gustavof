#!/bin/bash

# Configurações básicas
BASE_HOST="andromeda.lasdpc.icmc.usp.br"
USERNAME="gustavo"
REMOTE_DIR="/home/gustavo/load-test/k6"
total_tests=4 

# 12
PORTS=(
    2361
    2362
    2363
    2364
    2381
    2382
    2383
    2384
    2391
    2392
    # 2393
    # 2394
)


# Validação das configurações
if [ -z "$BASE_HOST" ] || [ -z "$USERNAME" ] || [ ${#PORTS[@]} -eq 0 ]; then
    echo "Erro: Configurações incompletas"
    exit 1
fi