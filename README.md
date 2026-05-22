# 🔍 Advanced Port Scanner

A high-performance multithreaded TCP port scanner built 
in Python — no Nmap dependency. Features service 
fingerprinting, banner grabbing, risk assessment, 
and automated HTML report generation.

---

## ✨ Features
- Multithreaded scanning (100+ threads)
- Service identification for 20+ common ports
- Banner grabbing to fingerprint running services
- Risk level flagging (HIGH / MEDIUM / LOW)
- Automated HTML report generation
- Clean CLI with colored output

---

## 🖥️ Terminal Output
![Terminal]<img width="733" height="364" alt="Screenshot 2026-05-22 162116" src="https://github.com/user-attachments/assets/98bbe588-116d-49d8-9e8b-56806e6e775f" />

---

## 📊 HTML Report
![Report]<img width="1902" height="709" alt="report" src="https://github.com/user-attachments/assets/2f5f7b06-33af-41fc-8296-ec201b50f314" />


---

## 🛠️ Installation
\```bash
git clone https://github.com/manikantakoka99/Advanced-Port-Scanner
cd Advanced-Port-Scanner
pip3 install jinja2 colorama --break-system-packages
\```

---

## 🚀 Usage
\```bash
# Basic scan
python3 main.py -t <target>

# Custom port range  
python3 main.py -t <target> -s 1 -e 65535

# More threads (faster)
python3 main.py -t <target> -th 200

# Legal test target (Nmap's official test host)
python3 main.py -t scanme.nmap.org -s 1 -e 1024
\```

---

## 📁 Project Structure
\```
port_scanner/
├── main.py
├── modules/
│   ├── scanner.py    # Multithreaded port scanning
│   ├── banner.py     # Banner grabbing + risk flagging
│   └── report.py     # HTML report generation
└── reports/          # Output reports saved here
\```

---

## 🔍 Sample Results (scanme.nmap.org)
| Port | Service | Risk | Banner |
|------|---------|------|--------|
| 22 | SSH | MEDIUM | OpenSSH 6.6.1p1 Ubuntu |
| 80 | HTTP | LOW | Apache/2.4.7 Ubuntu |

---

## ⚠️ Legal Disclaimer
This tool is for **educational purposes only.**
Only scan systems you **own** or have **explicit 
written permission** to test.
Unauthorized scanning is illegal.

---

## 🧰 Tech Stack
Python | Socket | Threading | Jinja2 | Colorama

---

## 👤 Author
**Manikanta Koka**  
[LinkedIn](https://www.linkedin.com/in/manikanta-koka-7524b3211/) | 
[GitHub](https://github.com/manikantakoka99)
