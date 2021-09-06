# gpu-utilization-metric-exporter
 A Prometheus exporter to export the GPU memory utilization of the Kubernetes cluster (only the GPUs being used) as a metric to be monitored.
 
## What is GPU memory utilization?
__GPU memory utilization__ represents the *percentage of time over the last second that the GPU’s memory controller was being utilized to either read or write from memory*.
One use-case for monitoring a cluster's GPU memory utilization could be to make a __scaling decision__. The observed memory utilization value would be pitched against a user-defined target memory utilization value and a decision to scale up or down could be made according to how heavily or underutilized the cluster's GPUs are. 

## Why is it required?
GPU utilization metrics aren't readily available on all Kubernetes platforms. One approach to use GPU utilization metrics is to use the metrics provided by NVIDIA DCGM. The DCGM exporters expose the GPU metrics (in Prometheus format) leveraging NVIDIA DCGM. The metrics are then scraped by a Prometheus server and made available for monitoring. The memory utilization values for each GPU is exposed as an *instant-vector metric* - **DCGM_FI_DEV_MEM_COPY_UTIL**.

We know that Prometheus provides a functional query language called PromQL. It allows the user to select and aggregate time series data in real time. However, the scope of the querying functionality restricts the user from performing complicated data manipulations  - manipulations which generally require the use of scripts. 
In our case since we require the GPU utilization value of all the GPUs in the system. Simply running the PromQL aggregator functions on the DCGM_FI_DEV_MEM_COPY_UTIL metric PromQL Functions such as - sum, sum_over_time, avg, avg_over_time, etc. will return the aggregated memory utilization values for all the GPUs targeted by the DCGM service. This means that if a GPU is not being utilized, but is targeted by the service, its utilization value (0%) will be added to the aggregate. This Project uses a custom python script which calculates the GPU memory utilization value for only the GPUs currently being utilized. The calculated metric is then made available for the Prometheus s#rver to scrape.  

## How does it Work?
The following figure describes the architecture of the system:

![Exporter Architecture](https://github.com/siddharth-mitra/gpu-utilization-metric-exporter/blob/main/images/custom-exporter.png)

The solution relies on the Data Center GPU Manager(DCGM) exporters to pull and make available GPU related metrics. These metrics are then scraped by the Prometheus server, where they are stored in a time series database. To compute the GPU memory utilization value of only the GPU resources being utilized at thaat instant, a component named 'custom exporter' is used. The component contains a python script running in a container. The script computes the GPU memory utilization of the GPU resources being utilized and makes them available for the prometheus server to scrape and store. Once the new metric is stored in the prometheus server, a prometheus adapter uses PromQL to compute the rolling average of the GPU memory utilization and exposes it as part of the custom metrics API endpoint. An HPA can then receive the average GPU memory utilization value by accessing this endpoint. 

