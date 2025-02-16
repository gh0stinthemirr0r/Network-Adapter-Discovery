# Network Dashboard

A simple Django application that displays network interface statistics (including throughput) and exposes them via a Prometheus-compatible endpoint.

## Features

- **Dashboard View**: Shows each network interface, its IP addresses, speed, status, and real-time I/O counters (bytes, packets, errors, drops).
- **Prometheus Integration**: Metrics available at `/metrics` so that Prometheus can scrape data and visualize it in Grafana or other tools.

## Requirements

- Python 3.7+
- Django
- psutil
- prometheus-client

Install these requirements using:
```bash
pip install django psutil prometheus-client
```
Requirements:
pip install django psutil prometheus-client
