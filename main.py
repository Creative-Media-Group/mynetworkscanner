from scapy.all import ARP, Ether, srp
import socket


def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "N/A"


def scan_network(ip_range):
    # Erstellen Sie eine ARP-Anfrage
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Senden Sie das Paket und erhalten Sie die Antwort
    result = srp(packet, timeout=3, verbose=0)[0]

    # Liste der gefundenen Geräte
    devices = []

    for sent, received in result:
        hostname = get_hostname(received.psrc)
        devices.append(
            {"ip": received.psrc, "mac": received.hwsrc, "hostname": hostname}
        )

    return devices


# Beispiel-IP-Bereich (passen Sie diesen an Ihr Netzwerk an)
ip_range = "192.168.1.1/24"
devices = scan_network(ip_range)

# Ausgabe der gefundenen Geräte
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}, Hostname: {device['hostname']}")
