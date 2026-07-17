#!/bin/bash
# Setup script for XSS Testing Tool

echo -e "\033[36m"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           XSS Tool Setup Script                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

# Make scripts executable
echo -e "\033[33m[*] Setting permissions...\033[0m"
chmod +x xss_tool.sh
chmod +x xss_tool.py
chmod +x quick_scan.py
chmod +x batch_scan.py

# Install dependencies
echo -e "\033[33m[*] Installing Python dependencies...\033[0m"
pip3 install -r requirements.txt

echo -e "\033[32m[+] Setup complete!{Colors.RESET}"
echo ""
echo -e "\033[33mUsage Examples:{Colors.RESET}"
echo "  ./xss_tool.sh -u http://target.com/?id=1"
echo "  python3 xss_tool.py -u http://target.com/?id=1 -s advanced"
echo "  python3 quick_scan.py http://target.com/?id=1"
echo "  python3 batch_scan.py targets.txt"
echo ""
