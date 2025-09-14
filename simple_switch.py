class SimpleSwitch:
    def __init__(self):
        self.mac_table = {}  # {mac: port}

    def receive_frame(self, src_mac, dst_mac, port):
        # Learn source MAC
        self.mac_table[src_mac] = port
        print(f"Learned MAC {src_mac} on port {port}")
        
        # Forward based on dst MAC
        if dst_mac in self.mac_table:
            forward_port = self.mac_table[dst_mac]
            if forward_port != port:
                print(f"Forwarding frame from port {port} to port {forward_port}")
            else:
                print("Frame is a loop, drop it")
        else:
            print(f"Flooding frame to all ports except {port}")

    def show_table(self):
        print("MAC Table:")
        for mac, port in self.mac_table.items():
            print(f"{mac} -> {port}")

# Test
if __name__ == "__main__":
    switch = SimpleSwitch()
    # Broadcast frame (dst is broadcast MAC)
    switch.receive_frame("00:1A:2B:3C:4D:5E", "FF:FF:FF:FF:FF:FF", 1)
    # Unicast to unknown dst
    switch.receive_frame("00:1A:2B:3C:4D:5E", "00:5E:6F:7A:8B:9C", 1)
    # Response from B to A (known dst)
    switch.receive_frame("00:5E:6F:7A:8B:9C", "00:1A:2B:3C:4D:5E", 2)
    switch.show_table()