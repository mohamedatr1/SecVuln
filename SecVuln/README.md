<div align="center">

```
  ███████╗███████╗ ██████╗██╗   ██╗██╗   ██╗██╗     ███╗   ██╗
  ██╔════╝██╔════╝██╔════╝██║   ██║██║   ██║██║     ████╗  ██║
  ███████╗█████╗  ██║     ██║   ██║██║   ██║██║     ██╔██╗ ██║
  ╚════██║██╔══╝  ██║     ╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║
  ███████║███████╗╚██████╗ ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║
  ╚══════╝╚══════╝ ╚═════╝  ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝
```

### AI-Driven Penetration Testing Agent · OSCP Methodology

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_DAG-FF6B35?style=for-the-badge&logo=graphql&logoColor=white)](https://github.com/langchain-ai/langgraph)
[![OpenAI](https://img.shields.io/badge/GPT--4o--mini-GitHub_Models-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/marketplace/models)
[![nmap](https://img.shields.io/badge/nmap-7.x-4EAA25?style=for-the-badge&logo=linux&logoColor=white)](https://nmap.org/)
[![License](https://img.shields.io/badge/License-MIT-DC143C?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-00D26A?style=for-the-badge&logo=statuspage&logoColor=white)]()
[![OSCP](https://img.shields.io/badge/Methodology-OSCP-FF0000?style=for-the-badge&logo=hackthebox&logoColor=white)]()
[![MITRE](https://img.shields.io/badge/Framework-MITRE_ATT%26CK-003087?style=for-the-badge&logo=mitre&logoColor=white)](https://attack.mitre.org/)

<br/>

> **SecVuln** is a fully autonomous AI-powered penetration testing pipeline — from network reconnaissance to CVE analysis and lateral movement mapping — all in a single command.

<br/>


</div>

---

> [!CAUTION]
> **Legal Disclaimer:** SecVuln is intended **exclusively** for authorized security testing, CTF competitions, and educational research. You must have **explicit written permission** before scanning any target. Unauthorized use may violate local, national, and international law. The authors assume **no liability** for misuse.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#️-architecture)
- [Pipeline Nodes](#-pipeline-nodes)
- [Terminal Output Preview](#-terminal-output-preview)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#️-usage)
- [Configuration](#️-configuration)
- [Evasion Reference](#-evasion-techniques-reference)
- [Project Structure](#️-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

**SecVuln** automates the full penetration testing reconnaissance phase using a clean **3-node stateful DAG** built with [LangGraph](https://github.com/langchain-ai/langgraph). It chains together `nmap` for discovery, NSE scripts for deep vulnerability fingerprinting, and **GPT-4o-mini** (via GitHub Models) for intelligent CVE analysis, Metasploit module lookup, and attack prioritization — all with colored terminal output and zero manual steps.

```
python main.py 45.33.32.156
```

That single command triggers the full pipeline and delivers a structured pentest report.

---

## ✨ Features

<table>
<tr>
<td width="50%">

**🔍 Smart Multi-Strategy Recon**
Runs nmap with an automatic fallback chain until open ports are found:
`SYN Scan → Full SYN (-p-) → TCP Connect → Fragmented MTU`

**🧬 NSE Deep Vulnerability Scanning**
Automatically runs `vulners`, `vuln`, `auth`, and `default` NSE scripts on every detected open port — only when ports exist.

**🤖 AI-Powered CVE Intelligence**
Sends the full combined scan payload to GPT-4o-mini for CVE identification, Metasploit module paths, Searchsploit commands, and a prioritized attack plan.

</td>
<td width="50%">

**🎨 Colored Terminal Output**
Full ANSI color system with semantic log levels: `[*] info`, `[+] success`, `[!] warning`, `[ERROR]`, `[SYSTEM]`, and section dividers.

**🔄 Stateful LangGraph DAG**
3-node pipeline with typed state (`SecurityState`) passed cleanly between nodes — fully extensible.

**🛡️ Advanced Evasion Support**
Packet fragmentation, MTU tuning (`--mtu 32`), source port spoofing (`--source-port 53`), scan delay, and random data padding — all configurable.

</td>
</tr>
</table>

---

## 🏗️ Architecture

SecVuln is a **3-node stateful Directed Acyclic Graph (DAG)** compiled by LangGraph. Each node receives and returns a typed `SecurityState` dict.

```
┌─────────────────────────────────────────────────────────────────┐
│                        SecVuln Pipeline                         │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Input: target_ip (CLI arg or interactive prompt)       │   │
│   └───────────────────────────┬─────────────────────────────┘   │
│                               │                                 │
│                               ▼                                 │
│   ┌───────────────────────────────────────────────────────────┐ │
│   │  🔎  NODE 1 — Reconnaissance Engine                       │ │
│   │                                                           │ │
│   │  Primary:   nmap -Pn -sS -sV -sC -T4 --open              │ │
│   │  Fallback1: nmap -Pn -sS -p- --min-rate=500              │ │
│   │  Fallback2: nmap -Pn -sT -p- --min-rate=500              │ │
│   │  Fallback3: nmap -f --mtu 32 --scan-delay 200ms          │ │
│   │                                                           │ │
│   │  Output → recon_payload (raw nmap stdout)                 │ │
│   └───────────────────────────┬───────────────────────────────┘ │
│                               │                                 │
│                               ▼  (skipped if no open ports)     │
│   ┌───────────────────────────────────────────────────────────┐ │
│   │  🧬  NODE 2 — NSE Deep Vulnerability Scanner              │ │
│   │                                                           │ │
│   │  Scripts: vulners, vuln, auth, default                    │ │
│   │  Merges NSE output with recon_payload                     │ │
│   │                                                           │ │
│   │  Output → recon_payload (recon + NSE combined)            │ │
│   └───────────────────────────┬───────────────────────────────┘ │
│                               │                                 │
│                               ▼                                 │
│   ┌───────────────────────────────────────────────────────────┐ │
│   │  🤖  NODE 3 — AI Vulnerability Intelligence               │ │
│   │                                                           │ │
│   │  Model:  GPT-4o-mini (GitHub Models)                      │ │
│   │  Input:  Full scan payload                                │ │
│   │  Output: CVEs · Metasploit · Searchsploit · Attack Plan   │ │
│   │                                                           │ │
│   │  Output → security_analysis (final report)                │ │
│   └───────────────────────────┬───────────────────────────────┘ │
│                               │                                 │
│                               ▼                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  Final Report printed to terminal                       │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### State Schema

```python
class SecurityState(TypedDict):
    target_ip:          str   # Target IP or hostname
    recon_payload:      str   # Accumulated scan output (recon + NSE merged)
    security_analysis:  str   # Final AI-generated pentest report
```

---

## 🔬 Pipeline Nodes

### 🔎 Node 1 — Reconnaissance Engine

The entry node executes nmap against the target using environment-configured options. If the primary scan returns no open ports, it automatically escalates through a **3-level fallback chain** without any user intervention:

| Priority | Strategy | Command Flags | Purpose |
|:---:|---|---|---|
| 1 | **Primary SYN** | `-sS -T4 --top-ports 1000` | Fast, stealthy default |
| 2 | **Full SYN** | `-sS -p- --min-rate=500` | All 65535 ports |
| 3 | **TCP Connect** | `-sT -p- --min-rate=500` | Firewall bypass fallback |
| 4 | **Fragmented** | `-f --mtu 32 --scan-delay 200ms --source-port 53` | Maximum evasion |

> Each stage is timed and its output size is reported. The first strategy that returns open ports stops the chain immediately.

---

### 🧬 Node 2 — NSE Deep Vulnerability Scanner

Activated **only if Node 1 found open ports.** Runs four NSE script categories simultaneously:

| Script | Category | Purpose |
|---|---|---|
| `vulners` | CVE Lookup | Maps service versions to known CVE database entries |
| `vuln` | Vulnerability Check | Actively tests for common vulnerabilities |
| `auth` | Authentication Bypass | Checks for default/empty credentials and auth weaknesses |
| `default` | Basic Enumeration | Service banners, SSL info, HTTP headers, SMB shares |

NSE output is merged with the recon payload into a single structured block before being passed to Node 3. On timeout or failure, Node 2 gracefully continues with recon data only.

---

### 🤖 Node 3 — AI Vulnerability Intelligence

Sends the full combined payload to **GPT-4o-mini** via GitHub Models with a senior penetration tester system prompt. The AI is instructed to:

- Identify every open port and service with version precision
- Map services to confirmed CVEs (CRITICAL / HIGH / MEDIUM / LOW)
- Provide exact **Metasploit module paths** (e.g., `exploit/multi/http/...`)
- Provide exact **Searchsploit commands** per vulnerability
- Flag misconfigurations: open auth, weak ciphers, exposed panels
- Produce a **numbered, prioritized attack plan**
- Suggest manual testing steps when no public exploit exists

> **Accuracy policy:** The AI is explicitly instructed to only cite CVEs it is 100% certain apply to the exact detected version. If uncertain, it states "No confirmed CVEs" and focuses on manual testing.

---

## 🖥️ Terminal Output Preview

```
  ███████╗███████╗ ██████╗██╗   ██╗██╗   ██╗██╗     ███╗   ██╗
  ...
  AI-Driven Penetration Testing Agent | OSCP Methodology
  ⚠  Always obtain written permission before scanning!

[?] Enter target IP or hostname: 45.33.32.156

[*] Target validated: 45.33.32.156
[*] Pipeline: Recon → NSE → AI Intelligence

[SYSTEM] Building SecVuln security analysis graph (3-node DAG)...
[SYSTEM] Graph compiled successfully. Ready to execute.

──────────────────────────────────────────────────────────────
  ▶  NODE 1 — Reconnaissance Engine
──────────────────────────────────────────────────────────────

[*] Starting reconnaissance on target: 45.33.32.156
[*] Running: nmap -Pn -sS -sV -sC -T4 --open --top-ports 1000 45.33.32.156
[+] Primary scan completed in 14.32s — 3847 bytes received

──────────────────────────────────────────────────────────────
  ▶  NODE 2 — NSE Deep Vulnerability Scanner
──────────────────────────────────────────────────────────────

[*] Open ports confirmed. Launching NSE scripts on: 45.33.32.156
[*] NSE command: nmap -Pn -sV --script vulners,vuln,auth,default -T4 45.33.32.156
[+] NSE Deep Scan completed in 47.18s

──────────────────────────────────────────────────────────────
  ▶  NODE 3 — AI Vulnerability Intelligence
──────────────────────────────────────────────────────────────

[*] Transmitting scan data to AI engine for deep analysis...
[+] AI analysis complete. Generating final report...

════════════════════════════════════════════════════════════
        SECVULN — AI PENETRATION TESTING REPORT
════════════════════════════════════════════════════════════

## Identified Services

| Port  | Service | Version                        |
|-------|---------|--------------------------------|
| 22    | SSH     | OpenSSH 6.6.1p1 Ubuntu        |
| 80    | HTTP    | Apache httpd 2.4.7 (Ubuntu)   |
| 3306  | MySQL   | MySQL 5.5.62-0ubuntu0.14.04.1 |

## Vulnerability Analysis

### [CRITICAL] CVE-2015-5600 — OpenSSH MaxAuthTries Bypass
- **Metasploit:** `auxiliary/scanner/ssh/ssh_login`
- **Searchsploit:** `searchsploit openssh 6.6`

### [HIGH] CVE-2017-7679 — Apache mod_mime Buffer Overread
- **Metasploit:** `exploit/multi/http/apache_mod_cgi_bash_env_exec`

## Prioritized Attack Plan
1. Brute-force SSH via Metasploit ssh_login or hydra
2. Enumerate HTTP with gobuster / dirb
3. Test MySQL for default credentials
...

──────────────────────────────────────────────────────────
  SecVuln | For authorized testing only | Stay ethical.
──────────────────────────────────────────────────────────
```

---

## 📋 Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.8+ | Tested on 3.10 and 3.12 |
| nmap | 7.x | Must be in `PATH` — `nmap --version` to verify |
| GitHub Models Token | — | Free tier available at [github.com/marketplace/models](https://github.com/marketplace/models) |

**Python packages** (installed via `requirements.txt`):

```
langchain-openai
langchain-core
langgraph
python-dotenv
```

---

## 🚀 Installation

**1. Clone the repository**

```bash
git clone --filter=blob:none --no-checkout https://github.com/mohamedatr1/Cyber-Core
cd Cyber-Core
git sparse-checkout init --no-cone
git sparse-checkout set SecVuln
git checkout
```

> 💡 No `git`? Download the ZIP from **Code → Download ZIP** on the repository page.

**2. Install nmap** (if not already installed)

```bash
# Debian / Ubuntu
sudo apt install nmap -y

# Fedora / RHEL
sudo dnf install nmap -y

# macOS (Homebrew)
brew install nmap

# Windows — download installer from https://nmap.org/download.html
```

**3. Create and activate a virtual environment**

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows PowerShell
venv\Scripts\Activate.ps1
```

**4. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**5. Configure your API token**

```bash
cp .env.example .env
```

Open `.env` and set your GitHub Models token:

```env
GITHUB_TOKEN=ghp_your_token_here
```

> 🔑 Get a free token at [github.com/settings/tokens](https://github.com/settings/tokens). The GitHub Models free tier is sufficient for most scans.

---

## ▶️ Usage

**Run with a target IP directly (recommended):**

```bash
python main.py 45.33.32.156
```

**Run interactively (prompted input):**

```bash
python main.py
# [?] Enter target IP or hostname: 45.33.32.156
```

**Run on a hostname:**

```bash
python main.py scanme.nmap.org
```

**Abort at any time:**

```
Ctrl+C   →  graceful exit with [!] Scan interrupted by user.
```

---

## ⚙️ Configuration

All behavior is controlled via **environment variables** — no code changes needed.

### Core Variables

| Variable | Default | Description |
|---|---|---|
| `GITHUB_TOKEN` | *(required)* | API key for GitHub Models · exits immediately if missing |
| `NMAP_PORTS` | `--top-ports 1000` | Port specification passed to nmap primary scan |
| `NMAP_SCAN_TYPE` | `-sS` | Primary scan type flag |
| `NMAP_EVASION` | *(empty)* | Extra evasion flags appended to primary command |

### Usage Examples

**Linux / macOS:**

```bash
# Scan specific ports only
export NMAP_PORTS="-p 22,80,443,8080,8443"
export NMAP_SCAN_TYPE="-sT"
python main.py 192.168.1.10

# Enable packet fragmentation on primary scan
export NMAP_EVASION="-f --mtu 32"
python main.py 10.0.0.5

# Full stealth mode — combine evasion + specific ports
export NMAP_SCAN_TYPE="-sT"
export NMAP_PORTS="-p-"
export NMAP_EVASION="--scan-delay 500ms --data-length 15"
python main.py 10.10.10.55
```

**Windows PowerShell:**

```powershell
$env:NMAP_PORTS = "-p 22,80,443"
$env:NMAP_SCAN_TYPE = "-sT"
python main.py 45.33.32.156
```

**Using a `.env` file:**

```env
GITHUB_TOKEN=ghp_your_token_here

# Nmap configuration
NMAP_PORTS=--top-ports 1000
NMAP_SCAN_TYPE=-sS
NMAP_EVASION=
```

> Variables in `.env` are loaded automatically at startup via `python-dotenv`. CLI environment variables always take precedence.

---

## 🔐 Evasion Techniques Reference

The **Fallback 3** fragmented packet scan uses these advanced anti-detection options. They can also be applied to the primary scan via `NMAP_EVASION`.

| Flag | Value | Purpose |
|---|---|---|
| `-f` | — | Fragment IP packets into 8-byte chunks to bypass DPI |
| `--mtu` | `32` | Force custom MTU — further splits packets to evade inspection |
| `--scan-delay` | `200ms` | Throttle probe rate to evade rate-based IDS/IPS |
| `--source-port` | `53` | Spoof source port as DNS — bypasses many stateless firewall rules |
| `--data-length` | `20` | Append random bytes to probe packets to mimic real traffic |
| `-T3` | — | Normal timing — reduces scan fingerprinting likelihood |
| `-Pn` | — | Skip host discovery — assumes host is up, avoids ICMP-blocking issues |

> These options are combined automatically in the fallback chain. The fragmented scan targets `--top-ports 100` to prevent timeouts.

---

## 🗂️ Project Structure

```
SecVuln/
├── main.py              # Entry point — LangGraph DAG, all 3 nodes, banner, CLI
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .env                 # Your local config (git-ignored)
└── README.md            # This file
```

> **Single-file design:** The entire pipeline — reconnaissance, NSE scanning, AI analysis, state graph, color system, banner, and CLI — lives in `main.py` for simplicity and portability.

---

## 🤝 Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

For major changes, **open an issue first** to discuss the proposal.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

---

<div align="center">

**Built for security professionals, bug bounty hunters, and CTF players.**

*Always hack ethically. Always get permission first.*

<br/>

[![GitHub stars](https://img.shields.io/github/stars/mohamedatr1/SecVuln?style=social)](https://github.com/mohamedatr1/SecVuln/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/mohamedatr1/SecVuln?style=social)](https://github.com/mohamedatr1/SecVuln/network/members)
[![GitHub issues](https://img.shields.io/github/issues/mohamedatr1/SecVuln?style=social)](https://github.com/mohamedatr1/SecVuln/issues)

</div>
