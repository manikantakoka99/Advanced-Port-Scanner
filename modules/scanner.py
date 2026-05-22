import socket
import threading
from queue import Queue
from datetime import datetime

# Thread-safe results list
results = []
results_lock = threading.Lock()

def scan_port(host, port, timeout=1):
    """Try to connect to a single port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0  # True if open
    except:
        return False

def worker(host, queue, open_ports):
    """Thread worker — pulls ports from queue"""
    while not queue.empty():
        port = queue.get()
        if scan_port(host, port):
            with results_lock:
                open_ports.append(port)
                print(f"  [+] Port {port} OPEN")
        queue.task_done()

def run_scan(host, start_port=1, end_port=1024, threads=100):
    """Main scan function"""
    print(f"\n[*] Scanning {host} ports {start_port}-{end_port}")
    print(f"[*] Threads: {threads}")
    print(f"[*] Started: {datetime.now().strftime('%H:%M:%S')}\n")

    # Resolve hostname to IP
    try:
        ip = socket.gethostbyname(host)
        print(f"[*] Resolved: {host} → {ip}\n")
    except socket.gaierror:
        print(f"[-] Cannot resolve {host}")
        return [], None

    # Fill queue with ports
    queue = Queue()
    for port in range(start_port, end_port + 1):
        queue.put(port)

    open_ports = []

    # Launch threads
    thread_list = []
    for _ in range(min(threads, end_port - start_port + 1)):
        t = threading.Thread(
            target=worker,
            args=(ip, queue, open_ports)
        )
        t.daemon = True
        t.start()
        thread_list.append(t)

    # Wait for all threads
    queue.join()

    open_ports.sort()
    print(f"\n[*] Scan complete: {len(open_ports)} open ports found")
    return open_ports, ip
