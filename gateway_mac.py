import socket, struct
import scapy.all as scapy

def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    routes = []
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
		continue

	    routes.append(socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))))
    
    print(routes)
    return routes

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

if __name__ == '__main__':
    default_gw = get_default_gateway_linux()
    
    for g in default_gw:
    	print(get_mac(g))
