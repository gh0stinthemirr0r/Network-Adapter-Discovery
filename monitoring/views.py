import psutil
from django.shortcuts import render
from django.http import HttpResponse
from prometheus_client import generate_latest
from .metrics import collect_network_metrics

def dashboard(request):
    """
    Render an HTML dashboard showing network interface stats.
    """
    # net_if_addrs() gets addresses; net_if_stats() gets additional details like speed, status, mtu
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)

    network_data = []
    for interface, addrs in addresses.items():
        # Gather addresses info
        ip_info = []
        for addr in addrs:
            ip_info.append({
                'family': str(addr.family),
                'address': addr.address,
                'netmask': addr.netmask,
                'broadcast': addr.broadcast,
            })
        
        # Gather stats info
        if interface in stats:
            iface_stats = stats[interface]
            speed = iface_stats.speed  # in Mbps (some OSes may return 0 if unknown)
            duplex = iface_stats.duplex
            mtu = iface_stats.mtu
            is_up = iface_stats.isup
        else:
            speed = 0
            duplex = 0
            mtu = 0
            is_up = False
        
        # Throughput from io_counters
        if interface in io_counters:
            iface_io = io_counters[interface]
            bytes_sent = iface_io.bytes_sent
            bytes_recv = iface_io.bytes_recv
            packets_sent = iface_io.packets_sent
            packets_recv = iface_io.packets_recv
            errin = iface_io.errin
            errout = iface_io.errout
            dropin = iface_io.dropin
            dropout = iface_io.dropout
        else:
            bytes_sent = bytes_recv = 0
            packets_sent = packets_recv = 0
            errin = errout = 0
            dropin = dropout = 0
        
        network_data.append({
            'interface': interface,
            'ip_info': ip_info,
            'speed': speed,
            'duplex': duplex,
            'mtu': mtu,
            'is_up': is_up,
            'bytes_sent': bytes_sent,
            'bytes_recv': bytes_recv,
            'packets_sent': packets_sent,
            'packets_recv': packets_recv,
            'errin': errin,
            'errout': errout,
            'dropin': dropin,
            'dropout': dropout,
        })

    return render(request, 'monitoring/dashboard.html', {'network_data': network_data})

def metrics(request):
    """
    Return Prometheus metrics for scraping.
    """
    registry = collect_network_metrics()
    return HttpResponse(generate_latest(registry), content_type="text/plain")
