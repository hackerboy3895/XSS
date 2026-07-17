#!/bin/bash
# XSS Attack Suite Launcher for Kali Linux

echo -e "\033[36m"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           XSS Attack Suite v3.0                             ║"
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

# Make all scripts executable
chmod +x *.py

# Run the appropriate tool based on argument
if [ $# -eq 0 ]; then
    echo -e "\033[32m[+] Starting XSS Attack Suite (Menu Mode)...\033[0m"
    python3 xss_suite.py
else
    case "$1" in
        1|basic)
            echo -e "\033[32m[+] Starting Basic XSS Scanner...\033[0m"
            python3 xss_tool.py "${@:2}"
            ;;
        2|advanced)
            echo -e "\033[32m[+] Starting Advanced XSS Scanner...\033[0m"
            python3 advanced_xss.py "${@:2}"
            ;;
        3|framework)
            echo -e "\033[32m[+] Starting Framework Scanner...\033[0m"
            python3 framework_scanner.py "${@:2}"
            ;;
        4|dom)
            echo -e "\033[32m[+] Starting DOM XSS Scanner...\033[0m"
            python3 advanced_xss.py "${@:2}" --dom-xss
            ;;
        5|payloads)
            echo -e "\033[32m[+] Starting Payload Generator...\033[0m"
            python3 payload_generator.py "${@:2}"
            ;;
        6|batch)
            echo -e "\033[32m[+] Starting Batch Scanner...\033[0m"
            python3 xss_tool.py "${@:2}"
            ;;
        7|exploit)
            echo -e "\033[32m[+] Starting Exploitation Mode...\033[0m"
            python3 advanced_xss.py "${@:2}" --exploit
            ;;
        8|help)
            echo -e "\033[33mUsage: ./xss_suite.sh [option] [args]\033[0m"
            echo ""
            echo "Options:"
            echo "  1|basic      - Basic XSS Scanner"
            echo "  2|advanced   - Advanced XSS Scanner (WAF Bypass)"
            echo "  3|framework  - Framework-Specific Scanner"
            echo "  4|dom        - DOM-Based XSS Scanner"
            echo "  5|payloads   - Payload Generator"
            echo "  6|batch      - Batch Scanner"
            echo "  7|exploit    - Exploitation Mode"
            echo "  8|help       - Show this help"
            echo ""
            echo "Examples:"
            echo "  ./xss_suite.sh"
            echo "  ./xss_suite.sh 2 -u http://target.com/?id=1"
            echo "  ./xss_suite.sh 3 http://target.com php"
            echo "  ./xss_suite.sh 5 html react"
            ;;
        *)
            echo -e "\033[31m[-] Unknown option: $1\033[0m"
            echo "Run './xss_suite.sh help' for usage"
            ;;
    esac
fi
