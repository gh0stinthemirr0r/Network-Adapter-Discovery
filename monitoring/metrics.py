import psutil
from prometheus_client import CollectorRegistry, Gauge

def collect_network_metrics():
    """
    Collect network metrics using psutil and populate
    a Prometheus CollectorRegistry with relevant gauges.
    """
    registry = CollectorRegistry()

    # Define gauges for network stats
    g_bytes_sent = Gauge('network_bytes_sent', 'Total bytes sent', ['interface'], registry=registry)
    g_bytes_recv = Gauge('network_bytes_recv', 'Total bytes received', ['interface'], registry=registry)
    g_packets_sent = Gauge('network_packets_sent', 'Total packets sent', ['interface'], registry=registry)
    g_packets_recv = Gauge('network_packets_recv', 'Total packets received', ['interface'], registry=registry)
    g_err_in = Gauge('network_err_in', 'Input errors', ['interface'], registry=registry)
    g_err_out = Gauge('network_err_out', 'Output errors', ['interface'], registry=registry)
    g_drop_in = Gauge('network_drop_in', 'Input drops', ['interface'], registry=registry)
    g_drop_out = Gauge('network_drop_out', 'Output drops', ['interface'], registry=registry)

    # Fetch I/O counters per NIC (interface)
    net_io = psutil.net_io_counters(pernic=True)

    for interface, stats in net_io.items():
        g_bytes_sent.labels(interface=interface).set(stats.bytes_sent)
        g_bytes_recv.labels(interface=interface).set(stats.bytes_recv)
        g_packets_sent.labels(interface=interface).set(stats.packets_sent)
        g_packets_recv.labels(interface=interface).set(stats.packets_recv)
        g_err_in.labels(interface=interface).set(stats.errin)
        g_err_out.labels(interface=interface).set(stats.errout)
        g_drop_in.labels(interface=interface).set(stats.dropin)
        g_drop_out.labels(interface=interface).set(stats.dropout)

    return registry
