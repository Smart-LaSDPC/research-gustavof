import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to parse JSON file with metrics
def parse_json_file(filepath):
    metrics = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                try:
                    metrics.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    return metrics

# Function to normalize metrics into a DataFrame
def normalize_metrics(metrics):
    normalized_data = []
    for metric in metrics:
        try:
            if metric.get('type') == 'Point':
                data = metric.get('data', {})
                normalized_data.append({
                    'metric': metric.get('metric'),
                    'name': data.get('name', metric.get('metric', 'unknown')),  # Use metric as default
                    'value': data.get('value'),
                    'time': data.get('time'),
                    'tags': data.get('tags', {})
                })
        except KeyError as e:
            print(f"KeyError: {e} in metric: {metric}")
    
    df = pd.DataFrame(normalized_data)
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    return df

# Function to visualize and save the data
def visualize_metrics(df, base_name, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not df.empty and df['value'].notna().any():
        colors = {
            'http_req_duration': 'blue',
            'http_reqs': 'green',
            'http_req_blocked': 'red',
            'http_req_connecting': 'purple',
            'http_req_tls_handshaking': 'orange',
            'http_req_sending': 'brown'
        }
        
        fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(12, 18), sharex=True)

        # Plot HTTP request duration
        sns.lineplot(data=df[df['name'] == 'http_req_duration'], x='time', y='value', marker='o', color=colors['http_req_duration'], ax=axes[0])
        axes[0].set_title('HTTP Request Duration')
        axes[0].set_ylabel('Duration (ms)')
        axes[0].grid(True)

        # Plot HTTP requests count
        sns.lineplot(data=df[df['name'] == 'http_reqs'], x='time', y='value', marker='o', color=colors['http_reqs'], ax=axes[1])
        axes[1].set_title('HTTP Requests Count')
        axes[1].set_ylabel('Requests Count')
        axes[1].grid(True)

        # Plot HTTP request blocked
        sns.lineplot(data=df[df['name'] == 'http_req_blocked'], x='time', y='value', marker='o', color=colors['http_req_blocked'], ax=axes[2])
        axes[2].set_title('HTTP Request Blocked Duration')
        axes[2].set_ylabel('Blocked Duration (ms)')
        axes[2].grid(True)

        # Plot HTTP request connecting
        sns.lineplot(data=df[df['name'] == 'http_req_connecting'], x='time', y='value', marker='o', color=colors['http_req_connecting'], ax=axes[3])
        axes[3].set_title('HTTP Request Connecting Duration')
        axes[3].set_ylabel('Connecting Duration (ms)')
        axes[3].grid(True)

        # Plot HTTP request TLS handshaking
        sns.lineplot(data=df[df['name'] == 'http_req_tls_handshaking'], x='time', y='value', marker='o', color=colors['http_req_tls_handshaking'], ax=axes[4])
        axes[4].set_title('HTTP Request TLS Handshaking Duration')
        axes[4].set_ylabel('TLS Handshaking Duration (ms)')
        axes[4].grid(True)

        # Plot HTTP request sending
        sns.lineplot(data=df[df['name'] == 'http_req_sending'], x='time', y='value', marker='o', color=colors['http_req_sending'], ax=axes[5])
        axes[5].set_title('HTTP Request Sending Duration')
        axes[5].set_ylabel('Sending Duration (ms)')
        axes[5].grid(True)

        plt.tight_layout()
        plt.savefig(f'{output_folder}/{base_name}_metrics.png')
    else:
        print("No valid data available for plotting.")

# Load and normalize data from multiple result files
def process_results(results_folder, output_folder):
    for filename in os.listdir(results_folder):
        if filename.endswith(".json"):
            result_filepath = os.path.join(results_folder, filename)
            print(f"Processing {result_filepath}")
            
            # Parse and normalize the metrics
            metrics = parse_json_file(result_filepath)
            df = normalize_metrics(metrics)

            # Extract the base name from the results file for naming
            base_name = filename.split('.')[0]
            
            # Visualize and save metrics
            visualize_metrics(df, base_name, output_folder)

if __name__ == "__main__":
    results_folder = 'log_results/'
    output_folder = 'parser_results/'
    process_results(results_folder, output_folder)