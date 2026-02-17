# 🔍 Subdomain Finder (subdomain.sh)

A lightweight and efficient **Bash** script designed for reconnaissance and passive subdomain discovery. This tool scrapes the HTML source of a target website, extracts unique subdomains, validates their status, and resolves them to their respective IP addresses.



## 🛠️ Features
- **Passive Discovery:** Scrapes subdomains directly from the target's web page source code.
- **Advanced Sanitization:** Automatically cleans URLs by removing query parameters (`?`), quotes (`'`), and commas (`,`) for high accuracy.
- **Live Validation:** Uses real-time `ping` checks to verify if the discovered subdomains are active (Alive).
- **IP Resolver:** Automatically extracts and maps unique IPv4 addresses for all valid subdomains.
- **Dependency-Free:** Built using native Linux tools (`wget`, `grep`, `strings`, `host`)—no additional libraries required.

## 🚀 Usage

1. **Grant Execution Permissions:**
   ```bash
   chmod +x subdomain.sh

2. **RUN The Script:**
    ```bash
    ./subdomain.sh <target_domain>
📁 Output Files:

The script generates three organized files in the working directory:

sub.txt: All unique domains found in the source code.

valid_sub.txt: Subdomains that responded successfully to the connectivity check.

ips.txt: A clean list of unique IP addresses for the active targets.

🔍 How it Works:

Fetch: Downloads the target's index page quietly using wget.

Extract: Uses strings to handle potential binary/compressed files and filters content for the specific target domain.

Clean: Trims JavaScript artifacts, HTML entities, and trailing characters to prevent false positives.

Resolve: Maps valid hosts to their server IPs using the host command and awk for clean output.

⚠️ Disclaimer:

This tool is for educational purposes and ethical penetration testing only. The developer is not responsible for any unauthorized or illegal use.
