# importing the requests library
import requests
import time
from prometheus_client import start_http_server, Gauge
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY


def get_gpu_utilization():
    gpu_utilization = []
    api_endpoint = "http://prometheus-operated.kfserving-monitoring:9090/api/v1/query"
    response = requests.get(api_endpoint, params={'query': 'DCGM_FI_DEV_MEM_COPY_UTIL'})
    results = response.json()['data']['result']
    for result in results:
        gpu_utilization.append(result['value'][1])

    for i in range(0, len(gpu_utilization)):
        gpu_utilization[i] = int(gpu_utilization[i])

    return gpu_utilization


def compute_average_utilization():
    gpus_utilized = []
    gpu_utilization = get_gpu_utilization()

    # Populate the gpus_utilized list with utilization values of GPUs being used.

    for gpu_util in gpu_utilization:
        if gpu_util != 0:
            gpus_utilized.append(gpu_util)

    # Compute the average of the gpus currently being utilized. Return 0 if no GPUs are being used.
    if len(gpus_utilized) == 0:
        return 0
    else:
        avg = sum(gpus_utilized) / len(gpus_utilized)
        return avg


class CustomCollector(object):
    def collect(self):
        avg_gpu_utilization = GaugeMetricFamily('avg_GPU_utilization',
                                                'Average GPU utilization of GPUs currently being used.')
        avg_gpu_utilization.add_metric([""], compute_average_utilization())
        yield avg_gpu_utilization


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)


