class SimpleSwitch:
    def __init__(self):
        self.mac_table = {}  # {vlan: {mac: port}}

    def receive_frame(self, src_mac, dst_mac, port, vlan_id=1):
        # Initialize VLAN table if not exists
        if vlan_id not in self.mac_table:
            self.mac_table[vlan_id] = {}
        # Learn source MAC
        self.mac_table[vlan_id][src_mac] = port
        print(f"Learned MAC {src_mac} on port {port} (VLAN {vlan_id})")
        
        # Forward based on dst MAC
        if dst_mac in self.mac_table.get(vlan_id, {}):
            forward_port = self.mac_table[vlan_id][dst_mac]
            if forward_port != port:
                print(f"Forwarding frame from port {port} to port {forward_port} (VLAN {vlan_id})")
            else:
                print("Frame is a loop, drop it")
        else:
            print(f"Flooding frame to all ports except {port} (VLAN {vlan_id})")

    def show_table(self):
        print("MAC Table:")
        for vlan, table in self.mac_table.items():
            print(f"VLAN {vlan}:")
            for mac, port in table.items():
                print(f"  {mac} -> {port}")

# Test
if __name__ == "__main__":
    switch = SimpleSwitch()
    # VLAN 1: Broadcast frame
    switch.receive_frame("00:1A:2B:3C:4D:5E", "FF:FF:FF:FF:FF:FF", 1, vlan_id=1)
    # VLAN 1: Unicast to unknown dst
    switch.receive_frame("00:1A:2B:3C:4D:5E", "00:5E:6F:7A:8B:9C", 1, vlan_id=1)
    # VLAN 2: Another device
    switch.receive_frame("00:AA:BB:CC:DD:EE", "FF:FF:FF:FF:FF:FF", 3, vlan_id=2)
    switch.show_table()