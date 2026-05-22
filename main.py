import argparse
from colorama import Fore, Style, init
from modules.scanner import run_scan
from modules.banner  import enrich_ports
from modules.report  import generate_report

init(autoreset=True)

def banner():
    print(Fore.CYAN + """
██████╗  ██████╗ ██████╗ ████████╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
██████╔╝██║   ██║██████╔╝   ██║   
██╔═══╝ ██║   ██║██╔══██╗   ██║   
██║     ╚██████╔╝██║  ██║   ██║   
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
    SCANNER — by Manikanta
    """ + Style.RESET_ALL)

def main():
    banner()

    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("-t",  "--target",     required=True, help="Target IP or domain")
    parser.add_argument("-s",  "--start",      type=int, default=1,    help="Start port")
    parser.add_argument("-e",  "--end",        type=int, default=1024, help="End port")
    parser.add_argument("-th", "--threads",    type=int, default=100,  help="Threads")
    parser.add_argument("--no-banner",         action="store_true",    help="Skip banner grab")
    parser.add_argument("--no-report",         action="store_true",    help="Skip report")
    args = parser.parse_args()

    # Run scan
    open_ports, ip = run_scan(
        args.target,
        args.start,
        args.end,
        args.threads
    )

    if not open_ports:
        print(Fore.RED + "[-] No open ports found or host unreachable")
        return

    # Banner grabbing
    enriched = open_ports
    if not args.no_banner:
        enriched = enrich_ports(ip, open_ports)

    # Generate report
    if not args.no_report and ip:
        generate_report(args.target, ip, enriched)

    # Summary
    print(Fore.GREEN + f"\n[✓] Done! Open ports: {[p['port'] for p in enriched]}")

if __name__ == "__main__":
    main()
