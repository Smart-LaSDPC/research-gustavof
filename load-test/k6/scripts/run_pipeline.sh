#!/bin/bash

# Array of test indices (0-based, matching the testPipeline array)
TESTS=(0 1)  # Adjust this array based on the number of tests in testPipeline

echo "=========================================="
echo "Starting Test Pipeline"
echo "Total tests to run: ${#TESTS[@]}"
echo "=========================================="

# Run each test with delay between them
for i in "${TESTS[@]}"
do
    echo -e "\n\n=========================================="
    echo "Starting Test $((i+1)) of ${#TESTS[@]}"
    echo "=========================================="

    k6 run --out json=results/logs/${test_type}_test_${VM_NAME}_test${i}_results.json \
        -e TEST_INDEX=$i \
        -e VM_PORT=$VM_PORT \
        -e VM_NAME=$VM_NAME \
        iot_test.js

    # If this isn't the last test, wait 2 minutes
    if [ $i -lt $((${#TESTS[@]}-1)) ]; then
        echo -e "\nWaiting 2 minutes before next test..."
        sleep 120
    fi
done

echo -e "\n=========================================="
echo "All tests completed"
echo "=========================================="