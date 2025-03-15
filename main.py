import socket
import subprocess


def is_host_up(ip):
    """Überprüft, ob ein Host erreichbar ist, indem ein Ping gesendet wird."""
    try:
        output = subprocess.check_output(
            ["ping", "-c", "1", "-W", "1", ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        return "1 received" in output
    except subprocess.CalledProcessError:
        return False


def get_hostname(ip):
    """Ermittelt den Hostnamen einer IP-Adresse."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "N/A"


def scan_network(ip_range_prefix, range_start=1, range_end=254):
    """Scannt das Netzwerk und gibt eine Liste der gefundenen Geräte zurück."""
    devices = []
    for i in range(range_start, range_end + 1):
        ip = f"{ip_range_prefix}.{i}"
        if is_host_up(ip):
            hostname = get_hostname(ip)
            devices.append({"ip": ip, "hostname": hostname})
    return devices


# Beispiel-IP-Bereich (passen Sie diesen an Ihr Netzwerk an)
ip_range_prefix = "192.168.1"
devices = scan_network(ip_range_prefix)

# Ausgabe der gefundenen Geräte
for device in devices:
    print(f"IP: {device['ip']}, Hostname: {device['hostname']}")
