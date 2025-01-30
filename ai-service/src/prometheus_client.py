import requests
import json
from datetime import datetime
import os
from src.config import Config


################################################################################
# Prometheus query function
################################################################################

class PrometheusMetrics:
    def __init__(self, config: Config):
        """Initialize PrometheusMetrics with configuration"""
        self.PROMETHEUS_URL = config.PROMETHEUS_URL
        
        self.QUERIES = {
            "request_count": "sum(rate(nginx_ingress_controller_requests[1m]))",
            "response_time_avg": "avg(rate(nginx_ingress_controller_response_duration_seconds_sum[1m]))",
            "response_time_p95": "histogram_quantile(0.95, sum(rate(nginx_ingress_controller_response_duration_seconds_bucket[1m])) by (le))",
            "active_connections": "avg(nginx_ingress_controller_nginx_connections_active)",
            "dropped_connections": "sum(rate(nginx_ingress_controller_nginx_connections_dropped[1m]))",
        }
        
        self.LOOKBACK_WINDOWS = {
            "5m": 300,
            "15m": 900, 
            "30m": 1800,
            "1h": 3600,
            # "3h": 3600 * 3,
            # "6h": 3600 * 6,
            # "12h": 3600 * 12,
            # "1d": 86400,
            # "3d": 86400 * 3,
            # "7d": 86400 * 7
        }
    

    def query_prometheus(self, promql_query, start, end, step):
        """Execute a Prometheus query with error handling"""
        try:
            params = {
                "query": promql_query,
                "start": start,
                "end": end,
                "step": step,
            }
            response = requests.get(self.PROMETHEUS_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying Prometheus: {e}")
            return None

    def collect_metrics(self):
        """Collect metrics for all configured lookback windows"""
        aggregated_results = {}
        
        for period, seconds in self.LOOKBACK_WINDOWS.items():
            print(f"Aggregating metrics for {period}...")
            end_time = int(datetime.now().timestamp())
            start_time = end_time - seconds
            step = "60s" if seconds <= 3600 else "300s"
            
            metrics = {}
            for key, promql_query in self.QUERIES.items():
                data = self.query_prometheus(promql_query, start_time, end_time, step)
                if data:
                    metrics[key] = data["data"]["result"]
            
            aggregated_results[period] = metrics

        return {
            "detailed": aggregated_results,
            "compact": self._create_compact_summary(aggregated_results)
        }

    def _create_compact_summary(self, aggregated_results):
        """Create a compact summary of the metrics"""
        return {
            period: {
                metric: [
                    {
                        "labels": result["metric"],
                        "values": result["values"],
                    }
                    for result in results
                ]
                for metric, results in metrics.items()
            }
            for period, metrics in aggregated_results.items()
        }


################################################################################
# Save results as JSON and TXT
################################################################################

def save_metrics(metrics_data, base_path="./metrics", formats=None):
    """
    Save metrics data to files in specified formats
    
    Args:
        metrics_data (dict): Dictionary containing 'detailed' and 'compact' metrics
        base_path (str): Base path for saving files
        formats (list): List of formats to save. Supported: ['json', 'txt']. 
                       If None, saves in all formats
    """
    # Create directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)
    
    if formats is None:
        formats = ['json', 'txt']
    
    formats = [f.lower() for f in formats]  # normalize format names
    
    for fmt in formats:
        if fmt not in ['json', 'txt']:
            print(f"Warning: Unsupported format '{fmt}' ignored")
            continue
            
        if fmt == 'json':
            # Save detailed results as JSON
            with open(f"{base_path}/nginx_metrics.json", "w") as json_file:
                json.dump(metrics_data["detailed"], json_file, indent=2)
            
            # Save compact results as JSON
            with open(f"{base_path}/nginx_metrics_compact.json", "w") as compact_file:
                json.dump(metrics_data["compact"], compact_file, indent=2)
                
        elif fmt == 'txt':
            # Save detailed results as TXT
            with open(f"{base_path}/nginx_metrics.txt", "w") as txt_file:
                txt_file.write(json.dumps(metrics_data["detailed"], indent=2))
            
            # Save compact results as TXT
            with open(f"{base_path}/nginx_metrics_compact.txt", "w") as txt_file:
                txt_file.write(json.dumps(metrics_data["compact"], indent=2))


def load_metrics_summary(file_path="nginx_metrics_compact.json"):
    """Load metrics summary from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing metrics summary
        
    Returns:
        dict: Loaded metrics summary
        
    Raises:
        FileNotFoundError: If the specified file is not found
    """
    try:
        with open(file_path, "r") as compact_file:
            return json.load(compact_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} not found")

if __name__ == "__main__":
    from src.config import Config
    config = Config()
    metrics_collector = PrometheusMetrics(config.PROMETHEUS_URL)
    metrics_data = metrics_collector.collect_metrics()
    save_metrics(metrics_data, formats=['json'])