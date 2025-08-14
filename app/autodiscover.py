"""
ARP-based discovery for local networks.
This uses `scapy` if available; falls back to calling `arp -a` on system if scapy not installed.
Scapy is optional; to enable add `scapy==2.4.7` to requirements.
"""
import subprocess
from .models import Database
import re

class ArpDiscover:
    def __init__(self, db_path='data/rpi_nms.db'):
        self.db = Database(db_path)
        self.db.init_db()

    def _parse_arp_output(self, text):
        # parse `arp -a` lines like: ? (192.168.1.10) at 00:11:22:33:44:55 [ether] on eth0
        ips = []
        for line in text.splitlines():
            m = re.search(r'\(([\d.]+)\)', line)
            if m:
                ips.append(m.group(1))
        return ips

    def scan_iface(self):
        try:
            out = subprocess.check_output(['arp', '-a'], text=True, stderr=subprocess.DEVNULL)
            ips = self._parse_arp_output(out)
            for ip in ips:
                # mark alive; name unknown
                self.db.upsert_device(ip=ip, name=None, alive=True)
            return ips
        except Exception as e:
            print("[autodiscover] arp failed:", e)
            return []
