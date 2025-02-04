import sys
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def normalize_metrics(metrics):
    normalized_data = []
    for metric in metrics:
        try:
            if metric.get('type') == 'Point':
                data = metric.get('data', {})
                normalized_data.append({
                    'metric': metric.get('metric'),
                    'name': data.get('name', metric.get('metric', 'unknown')),
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

def visualize_metrics(df, port, test_type):
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
        axes[0].set_title(f'HTTP Request Duration - VM {port}')
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
        
        # Garante que o diretório de gráficos existe
        os.makedirs('results/graphs', exist_ok=True)
        
        # Salva o gráfico com o nome padronizado
        output_file = f'results/graphs/{test_type}_test_vm{port}_metrics.png'
        plt.savefig(output_file)
        plt.close()
        
        print(f"Gráfico gerado com sucesso: {output_file}")
    else:
        print("No valid data available for plotting.")

def analyze_results(port, test_type):
    try:
        # Define o caminho do arquivo de resultados
        results_file = f"results/logs/{test_type}_test_vm{port}_results.json"
        
        # Verifica se o arquivo existe
        if not os.path.exists(results_file):
            print(f"Arquivo não encontrado: {results_file}")
            return
        
        # Parse e normaliza as métricas
        metrics = parse_json_file(results_file)
        df = normalize_metrics(metrics)
        
        # Visualiza e salva as métricas
        visualize_metrics(df, port, test_type)
        
    except Exception as e:
        print(f"Erro ao analisar resultados: {e}")
        return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python analyze_results.py <port> <test_type>")
        sys.exit(1)
    
    try:
        port = sys.argv[1]
        test_type = sys.argv[2]
        analyze_results(port, test_type)
    except Exception as e:
        print(f"Erro ao executar análise: {e}")
        sys.exit(1)