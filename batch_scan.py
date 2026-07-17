#!/usr/bin/env python3
"""
Batch XSS Scanner - Test multiple targets quickly
"""

import sys
import os
from xss_tool import XSSTester, banner
from colorama import init, Fore

init(autoreset=True)

def batch_scan(target_file, scan_type='basic'):
    banner()
    
    if not os.path.exists(target_file):
        print(f"{Fore.RED}[-] File not found: {target_file}{Fore.RESET}")
        return
    
    with open(target_file, 'r') as f:
        targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not targets:
        print(f"{Fore.RED}[-] No targets found in file{Fore.RESET}")
        return
    
    print(f"{Fore.CYAN}[*] Loaded {len(targets)} targets{Fore.RESET}\n")
    
    tester = XSSTester()
    
    for i, target in enumerate(targets, 1):
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"  Target {i}/{len(targets)}: {target}")
        print(f"{'='*60}{Fore.RESET}")
        
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        try:
            tester.scan_url(target, scan_type)
        except Exception as e:
            print(f"{Fore.RED}[-] Error scanning {target}: {e}{Fore.RESET}")
    
    tester.generate_report()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"{Fore.YELLOW}Usage: python batch_scan.py <targets_file> [scan_type]{Fore.RESET}")
        print(f"{Fore.YELLOW}Example: python batch_scan.py targets.txt advanced{Fore.RESET}")
        sys.exit(1)
    
    target_file = sys.argv[1]
    scan_type = sys.argv[2] if len(sys.argv) > 2 else 'basic'
    
    batch_scan(target_file, scan_type)
