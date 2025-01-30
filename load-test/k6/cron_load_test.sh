#!/bin/bash

# Define the number of iterations (based on your testPipeline length)
NUM_TESTS=5

# Run each test configuration
for i in $(seq 0 $((NUM_TESTS-1)))
do
  echo "Running test $((i+1)) of $NUM_TESTS"
  
  # Set the ITERATION_INDEX and run the k6 test, outputting logs to a file
  ITERATION_INDEX=$i k6 run --out json=log_results/results_test_$i.json load_test_pipeline.js
  
  echo "Test $((i+1)) completed, results saved to results_test_$i.json"
done