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
    while True:
        try:
            src_mac = input("Enter source MAC (e.g., 00:1A:2B:3C:4D:5E) or 'quit' to exit: ")
            if src_mac.lower() == 'quit':
                break
            dst_mac = input("Enter destination MAC (e.g., 00:5E:6F:7A:8B:9C): ")
            port = int(input("Enter port number (1-10): "))
            vlan_id = int(input("Enter VLAN ID (1-4094): "))
            switch.receive_frame(src_mac, dst_mac, port, vlan_id)
            switch.show_table()
        except ValueError:
            logger.error("Invalid input: Port and VLAN must be numbers")
        except Exception as e:
            logger.error(f"Error: {e}")