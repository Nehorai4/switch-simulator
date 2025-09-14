import logging

# הגדרת לוגינג
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleSwitch:
    def __init__(self):
        self.mac_table = {}  # {vlan: {mac: port}}
        logger.info("Switch initialized with empty MAC table")

    def receive_frame(self, src_mac, dst_mac, port, vlan_id=1):
        # בדיקה אם VLAN חדש, יצירת טבלה ריקה אם צריך
        if vlan_id not in self.mac_table:
            self.mac_table[vlan_id] = {}
        # למידת MAC מקור
        self.mac_table[vlan_id][src_mac] = port
        logger.info(f"Learned MAC {src_mac} on port {port} (VLAN {vlan_id})")
        
        # העברת פריים לפי MAC יעד
        if dst_mac in self.mac_table.get(vlan_id, {}):
            forward_port = self.mac_table[vlan_id][dst_mac]
            if forward_port != port:
                logger.info(f"Forwarding frame from port {port} to port {forward_port} (VLAN {vlan_id})")
            else:
                logger.warning("Frame is a loop, drop it")
        else:
            logger.info(f"Flooding frame to all ports except {port} (VLAN {vlan_id})")

    def show_table(self):
        logger.info("MAC Table:")
        for vlan, table in self.mac_table.items():
            logger.info(f"VLAN {vlan}:")
            for mac, port in table.items():
                logger.info(f"  {mac} -> {port}")

# בדיקה
if __name__ == "__main__":
    switch = SimpleSwitch()
    # פריים שידור ב-VLAN 1
    switch.receive_frame("00:1A:2B:3C:4D:5E", "FF:FF:FF:FF:FF:FF", 1, vlan_id=1)
    # Unicast ליעד לא מוכר ב-VLAN 1
    switch.receive_frame("00:1A:2B:3C:4D:5E", "00:5E:6F:7A:8B:9C", 1, vlan_id=1)
    # מכשיר חדש ב-VLAN 2
    switch.receive_frame("00:AA:BB:CC:DD:EE", "FF:FF:FF:FF:FF:FF", 3, vlan_id=2)
    switch.show_table()