# Define variables
LOGS_DIR = log_results
PARSER_DIR = parser_results

# Ensure results directory exists
init:
	mkdir -p $(LOGS_DIR) && mkdir -p $(PARSER_DIR)

# Run the load test pipeline and save results
load:
	bash cron_load_test.sh

parse:
	bash cron_parser.sh