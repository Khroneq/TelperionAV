from scapy.all import sniff
from utils.logger import log
from utils.config import load_config

def packet_callback(packet):
    if packet.haslayer('IP'):
        log(f"Network activity detected: {packet['IP'].src} -> {packet['IP'].dst}")

def start_network_monitor():
    config = load_config()
    if config['network_monitoring']:
        log("Starting network monitoring...")
        sniff(prn=packet_callback, store=0)