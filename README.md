# gpu-utilization-metric-exporter
 A Prometheus exporter to export the GPU memory utilization of the system as a metric to be monitored.
 
## What is GPU memory utilization?
GPU memory utilization represents the percentage of time over the last second that the GPU’s memory controller was being utilized to either read or write from memory.

## Why is it required?
GPU utilization metrics aren't readily available on all Kubernetes platforms. One way to use the GPU utilization metrics is to use the metrics provided by NVIDIA DCGM. The DCGM exporters expose the GPU metrics (in the Prometheus format) leveraging NVIDIA DCGM. The metrics are then scraped by the Prometheus server and made available for monitoring. The memory utilization values for each GPU is exposed as the instant-vector metric - DCGM_FI_DEV_MEM_COPY_UTIL.

We know that Prometheus provides a functional query language called PromQL. It allows the user to select and aggregate time series data in real time. However, the scope of the querying functionality restricts the user from performing complicated data manipulations  - manipulations which generally require the use of scripts. 
In our case since we require the GPU utilization value of all the GPUs in the system. Simply running the PromQL aggregator functions on the DCGM_FI_DEV_MEM_COPY_UTIL metric (avg, avg_over_time, etc) will return the aggregated memory utilization values for all the GPUs targeted by the DCGM service. This means that if a GPU is not being utilized, but is targeted by the service, its utilization value (0%) will be added to the net utilization value.
This projects uses a custom python script which calculates the GPU memory utilization value for only the GPUs currently being utilized. Then makes the calcluated metric available for the Prometheus server to scrape.  

## Architecture
![Exporter Architecture](https://github.com/siddharth-mitra/gpu-utilization-metric-exporter.git/images/custom-exporter.png)

