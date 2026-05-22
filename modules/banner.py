import socket

# Common port → service name mapping
PORT_SERVICES = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    135:  "RPC",
    139:  "NetBIOS",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    993:  "IMAPS",
    995:  "POP3S",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017:"MongoDB"
}

def grab_banner(host, port, timeout=2):
    """Try to grab service banner"""
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, port))

        # Send HTTP request for web ports
        if port in [80, 8080, 8443, 443]:
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")

        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner[:200] if banner else "No banner"

    except:
        return "No banner"

def get_service(port):
    """Return service name for port"""
    return PORT_SERVICES.get(port, "Unknown")

def enrich_ports(host, open_ports):
    """Get service + banner for all open ports"""
    print("\n[*] Grabbing banners...")
    enriched = []

    for port in open_ports:
        service = get_service(port)
        banner  = grab_banner(host, port)
        enriched.append({
            "port":    port,
            "service": service,
            "banner":  banner,
            "risk":    get_risk(port)
        })
        print(f"  [+] {port}/{service} → {banner[:60]}")

    return enriched

def get_risk(port):
    """Flag risky ports"""
    high_risk = [21, 23, 135, 139, 445, 3389, 5900]
    med_risk  = [22, 25, 53, 3306, 5432, 6379, 27017]

    if port in high_risk:
        return "HIGH"
    elif port in med_risk:
        return "MEDIUM"
    else:
        return "LOW"
