import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scapy.all import *
from collections import defaultdict
import time
from datetime import datetime
import threading
import warnings
import logging
from typing import Dict, List, Optional
import socket
from streamlit_autorefresh import st_autorefresh
from scapy.all import sniff, conf, get_if_list
from scapy.all import sniff, conf, get_if_list, ARP, IP, TCP, UDP
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.http import HTTPRequest  # pip install scapy-http




# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PacketProcessor:
    """Process and analyze network packets"""

    def __init__(self):
        self.protocol_map = {
            1: 'ICMP',
            6: 'TCP',
            17: 'UDP',
            'ARP': 'ARP',
            'DNS': 'DNS',
            'HTTP': 'HTTP',
            'HTTPS': 'HTTPS'
        }
        self.packet_data = []
        self.start_time = datetime.now()
        self.packet_count = 0
        self.lock = threading.Lock()

    def get_protocol_name(self, protocol_num: int) -> str:
        """Convert protocol number to name"""
        return self.protocol_map.get(protocol_num, f'OTHER({protocol_num})')

    def process_packet(self, packet) -> None:
        """Process a single packet and extract relevant information"""
        try:
            # ————————————— ARP first —————————————
            if ARP in packet:
                with self.lock:
                    pkt = packet[ARP]
                    self.packet_data.append({
                        'timestamp': datetime.now(),
                        'source': pkt.psrc,
                        'destination': pkt.pdst,
                        'protocol': 'ARP',
                        'size': len(packet),
                        'time_relative': (datetime.now() - self.start_time).total_seconds(),
                        # for ARP you could add:
                        'hwsrc': pkt.hwsrc,
                        'hwdst': pkt.hwdst
                    })
                    self.packet_count += 1
                return  # done

            # ————————— IP-layer protocols next ————————
            if IP in packet:
                with self.lock:
                    ip = packet[IP]
                    base_proto = self.get_protocol_name(ip.proto)
                    info = {
                        'timestamp': datetime.now(),
                        'source': ip.src,
                        'destination': ip.dst,
                        'protocol': base_proto,
                        'size': len(packet),
                        'time_relative': (datetime.now() - self.start_time).total_seconds(),
                    }

                    # ——— DNS (usually UDP 53, but could be TCP 53) ———
                    if packet.haslayer(DNS) and packet.haslayer(DNSQR):
                        dns = packet[DNSQR]
                        info.update({
                            'protocol': 'DNS',
                            'dns_query': dns.qname.decode().rstrip('.')
                        })

                    # ——— HTTP (cleartext) ———
                    elif packet.haslayer(HTTPRequest):
                        http = packet[HTTPRequest]
                        info.update({
                            'protocol': 'HTTP',
                            'http_method': http.Method.decode(),
                            'http_host': http.Host.decode(),
                            'http_path': http.Path.decode()
                        })

                    # ——— HTTPS detection (encrypted, just port 443) ———
                    elif TCP in packet and (packet[TCP].dport == 443 or packet[TCP].sport == 443):
                        info['protocol'] = 'HTTPS'
                        # payload is encrypted, so we won’t parse further

                    # ——— TCP default ———
                    elif TCP in packet:
                        tcp = packet[TCP]
                        info.update({
                            'src_port': tcp.sport,
                            'dst_port': tcp.dport,
                            'tcp_flags': tcp.flags
                        })

                    # ——— UDP default ———
                    elif UDP in packet:
                        udp = packet[UDP]
                        info.update({
                            'src_port': udp.sport,
                            'dst_port': udp.dport
                        })

                    # append & trim
                    self.packet_data.append(info)
                    self.packet_count += 1
                    if len(self.packet_data) > 10000:
                        self.packet_data.pop(0)

        except Exception as e:
            logger.error(f"Error processing packet: {str(e)}")

    def get_dataframe(self) -> pd.DataFrame:
        """Convert packet data to pandas DataFrame, filling any missing columns."""
        with self.lock:
            df = pd.DataFrame(self.packet_data)

            # list all the optional keys we introduced in process_packet()
            optional_cols = [
                'hwsrc', 'hwdst',            # ARP
                'dns_query',                # DNS
                'http_method', 'http_host', 'http_path'  # HTTP
            ]

            # for each one, if it’s not in df yet, add it as a column of Nones
            for col in optional_cols:
                if col not in df.columns:
                    df[col] = None

            return df



def create_visualizations(df: pd.DataFrame):
    """Create all dashboard visualizations"""
    if len(df) > 0:
        # Protocol distribution
        protocol_counts = df['protocol'].value_counts()
        fig_protocol = px.pie(
            values=protocol_counts.values,
            names=protocol_counts.index,
            title="Protocol Distribution"
        )
        st.plotly_chart(fig_protocol, use_container_width=True)

        # After protocol pie:
        fig_extra = px.bar(
            x=protocol_counts.index,
            y=protocol_counts.values,
            title="All Protocol Counts"
        )
        st.plotly_chart(fig_extra, use_container_width=True)

        # Packets timeline
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df_grouped = df.groupby(df['timestamp'].dt.floor('S')).size()
        fig_timeline = px.line(
            x=df_grouped.index,
            y=df_grouped.values,
            title="Packets per Second",
            labels={
                'x': 'Time (s since start)',
                'y': 'Packets per Second'
            }
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Top source IPs
        top_sources = df['source'].value_counts().head(10)
        fig_sources = px.bar(
            x=top_sources.index,
            y=top_sources.values,
            title="Top Source IP Addresses"
        )
        st.plotly_chart(fig_sources, use_container_width=True)


def start_packet_capture(iface: str):
    processor = PacketProcessor()
    def capture_packets():
        sniff(iface=iface, prn=processor.process_packet, store=False, promisc=True)
    threading.Thread(target=capture_packets, daemon=True).start()
    return processor


# helper to format bytes
def format_bytes(size: int) -> str:
    for unit in ["B","KB","MB","GB","TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def main():
    """Main function to run the dashboard"""
    # auto-refresh every 2 seconds
    st_autorefresh(interval=2_000, key="packet_refresh")

    st.set_page_config(page_title="Network Traffic Analysis", layout="wide")
    st.title("Real-time Network Traffic Analysis")

    # 1) Auto-detect & dropdown
    default_iface = conf.route.route("8.8.8.8")[0]
    interfaces = get_if_list()
    default_index = interfaces.index(default_iface) if default_iface in interfaces else 0
    iface = st.sidebar.selectbox("📡 Capture interface", interfaces, index=default_index)

    # 2) Initialize session_state.iface
    if 'iface' not in st.session_state:
        st.session_state.iface = iface

    # 3) Detect changes
    if iface != st.session_state.iface:
        st.session_state.iface = iface
        st.session_state.processor = start_packet_capture(iface)
        st.session_state.start_time = time.time()

    # 4) Ensure processor exists
    if 'processor' not in st.session_state:
        st.session_state.processor = start_packet_capture(st.session_state.iface)
        st.session_state.start_time = time.time()


    # 5) Show which iface is active
    st.write(f"🐾 Capturing on interface: **{st.session_state.iface}**")

    # Create dashboard layout
    col1, col2 = st.columns(2)

    # Get current data
    df = st.session_state.processor.get_dataframe()

    # ——— Phase 2 widgets & filtering ———

    # 1) Protocol filter (now df exists, but may be empty)
    if not df.empty:
        available = df['protocol'].unique().tolist()
    else:
        available = ['TCP', 'UDP', 'ICMP', 'OTHER']

    selected_protos = st.sidebar.multiselect(
        "✔️ Protocols",
        available,
        default=available
    )

    # Now apply both filters
    if not df.empty:
        df = df[df['protocol'].isin(selected_protos)]

    # ——— 5-tuple flow aggregation ———
    required = {'source', 'destination', 'protocol', 'src_port', 'dst_port'}
    if not df.empty and required.issubset(df.columns):
        # now it’s safe to groupby
        flow_df = (
            df.groupby(
                ['source', 'destination', 'protocol', 'src_port', 'dst_port'],
                as_index=False
            )
            .agg(
                packet_count=('size', 'count'),
                total_bytes=('size', 'sum'),
                first_seen=('timestamp', 'min'),
                last_seen=('timestamp', 'max')
            )
        )
        flow_df = flow_df.sort_values('packet_count', ascending=False)
        flow_df['total_size'] = flow_df['total_bytes'].apply(format_bytes)
    else:
        flow_df = pd.DataFrame(
            columns=[
                'source', 'destination', 'protocol', 'src_port', 'dst_port',
                'packet_count', 'total_bytes', 'first_seen', 'last_seen', 'total_size'
            ]
        )

    # Display metrics
    with col1:
        st.metric("Total Packets", len(df))
    with col2:
        duration = time.time() - st.session_state.start_time
        st.metric("Capture Duration", f"{duration:.2f}s")

    # Display visualizations
    create_visualizations(df)

    display_cols = [
        "source", "src_port", "destination", "dst_port", "protocol",
        "packet_count", "first_seen", "last_seen"
    ]
    if 'total_size' in flow_df.columns:
        display_cols.insert(6, 'total_size')
    st.subheader("Top Network Flows")
    # show only the top 10
    st.dataframe(flow_df.head(10)[display_cols], use_container_width=True, hide_index=True)

    # Display recent packets
    st.subheader("Recent Packets")
    if len(df) > 0:
        st.dataframe(
            df.tail(10)[['timestamp', 'source', 'destination', 'protocol', 'size']],
            use_container_width=True, hide_index=True)

    # Add refresh button
    if st.button('Refresh Data'):
        st.rerun()

    # Auto refresh
    # time.sleep(5)
    # st.rerun()


if __name__ == "__main__":
    main()
