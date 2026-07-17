#!/bin/bash
# XSS Tool Launcher for Kali Linux

echo -e "\033[36m"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           XSS Penetration Testing Tool                      ║"
echo "║           For Authorized Security Testing Only              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

# Check if running as root (optional, but recommended for Kali)
if [ "$EUID" -ne 0 ]; then 
    echo -e "\033[33m[!] Warning: Not running as root. Some features may be limited.\033[0m"
fi

# Check Python version
python3 --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "\033[31m[-] Python 3 is required. Please install Python 3.\033[0m"
    exit 1
fi

# Check if requirements are installed
echo -e "\033[33m[*] Checking dependencies...\033[0m"
pip3 show requests > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "\033[33m[*] Installing required packages...\033[0m"
    pip3 install -r requirements.txt
fi

# Run the tool
echo -e "\033[32m[+] Starting XSS Tool...\033[0m"
python3 xss_tool.py "$@"
