### 1) Run your k6 load test with JSON output:
### k6 run --iterations <number_of_tests_in_pipeline> load_test_pipeline.js
k6 run --iterations 2 --out json=results/poisson_results.json load_test_pipeline.js
### 2) Run the Python script to parse the results and generate visualizations:
### python analyze_results.py

