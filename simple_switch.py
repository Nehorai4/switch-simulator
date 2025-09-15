import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('switch_log.txt')
    ]
)
logger = logging.getLogger(__name__)

class SimpleSwitch:
    def __init__(self):
        self.mac_table = {}  # {vlan: {mac: port}}
        self.frame_count = 0  # סופר פריימים
        logger.info("Switch initialized with empty MAC table")

    def receive_frame(self, src_mac, dst_mac, port, vlan_id=1):
        start_time = time.time()  # מתחיל למדוד זמן
        self.frame_count += 1
        if vlan_id not in self.mac_table:
            self.mac_table[vlan_id] = {}
        self.mac_table[vlan_id][src_mac] = port
        logger.info(f"Learned MAC {src_mac} on port {port} (VLAN {vlan_id})")
        
        if dst_mac in self.mac_table.get(vlan_id, {}):
            forward_port = self.mac_table[vlan_id][dst_mac]
            if forward_port != port:
                logger.info(f"Forwarding frame from port {port} to port {forward_port} (VLAN {vlan_id})")
            else:
                logger.warning("Frame is a loop, drop it")
        else:
            logger.info(f"Flooding frame to all ports except {port} (VLAN {vlan_id})")
        end_time = time.time()  # מסיים למדוד
        processing_time = end_time - start_time
        logger.info(f"Frame {self.frame_count} processed in {processing_time:.4f} seconds")

    def show_table(self):
        logger.info("MAC Table:")
        for vlan, table in self.mac_table.items():
            logger.info(f"VLAN {vlan}:")
            for mac, port in table.items():
                logger.info(f"  {mac} -> {port}")
        logger.info(f"Total frames processed: {self.frame_count}")

if __name__ == "__main__":
    switch = SimpleSwitch()
    switch.receive_frame("00:1A:2B:3C:4D:5E", "FF:FF:FF:FF:FF:FF", 1, vlan_id=1)
    switch.receive_frame("00:1A:2B:3C:4D:5E", "00:5E:6F:7A:8B:9C", 1, vlan_id=1)
    switch.receive_frame("00:AA:BB:CC:DD:EE", "FF:FF:FF:FF:FF:FF", 3, vlan_id=2)
    switch.show_table()