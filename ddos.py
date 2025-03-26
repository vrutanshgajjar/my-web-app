from scapy.all import sniff, wrpcap, IP
import time
from collections import Counter

# Global variables
packet_counter = Counter()
packets = []  # List to store packets
start_time = None  # Initialize to None

# Packet processing function
def process_packet(packet):
    global packets  # Access the global packets list
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        # Update counter
        packet_counter[src_ip] += 1

        # Save the packet
        packets.append(packet)

        # Print packet details
        print(f"Source: {src_ip} -> Destination: {dst_ip}")
    
    # Check for DDoS-like behavior
    detect_ddos()

def detect_ddos():
    global start_time, packets  # Access global variables
    current_time = time.time()
    
    # Initialize start_time if it's None
    if start_time is None:
        start_time = current_time
    
    duration = current_time - start_time
    if duration >= 60:  # Analyze every minute
        print("\n--- Analysis Report ---")
        for ip, count in packet_counter.items():
            print(f"{ip}: {count} packets")
            if count > 100:  # Threshold for suspicious activity
                print(f"[ALERT] Potential DDoS from {ip}")
        
        # Save captured packets to a .pcap file
        filename = f"captured_packets_{int(time.time())}.pcap"
        wrpcap(filename, packets)
        print(f"[INFO] Packets saved to {filename}")

        # Reset counters and packet list
        packet_counter.clear()
        packets = []
        start_time = current_time  # Reset the start time

# Main function to start packet sniffing
def start_sniffer(interface="Wi-Fi"):  # Replace "Wi-Fi" with your actual interface
    print(f"Starting packet capture on {interface}...")
    sniff(iface=interface, prn=process_packet, store=False, filter="ip")

if __name__ == "__main__":
    start_sniffer("Wi-Fi")  # Replace with the actual interface name
