import os
import sys
import shlex
import subprocess
import time
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
import re


# =================================================================
# ANSI COLOR CODES — Terminal output styling for SecVuln
# =================================================================
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GREY    = "\033[90m"

def info(msg: str):
    """Informational message — blue [*]"""
    print(f"{Color.BLUE}[*]{Color.RESET} {msg}")

def success(msg: str):
    """Success message — green [+]"""
    print(f"{Color.GREEN}[+]{Color.RESET} {msg}")

def warning(msg: str):
    """Warning message — yellow [!]"""
    print(f"{Color.YELLOW}[!]{Color.RESET} {msg}")

def error(msg: str):
    """Error message — red [ERROR]"""
    print(f"{Color.RED}[ERROR]{Color.RESET} {msg}")

def system(msg: str):
    """System/internal message — magenta [SYSTEM]"""
    print(f"{Color.MAGENTA}[SYSTEM]{Color.RESET} {msg}")

def section(title: str):
    """Prints a colored section divider with a title"""
    bar = "─" * 60
    print(f"\n{Color.CYAN}{bar}{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}  ▶  {title}{Color.RESET}")
    print(f"{Color.CYAN}{bar}{Color.RESET}\n")


# =================================================================
# BANNER — Displayed at startup
# =================================================================
BANNER = f"""
{Color.RED}{Color.BOLD}
  ███████╗███████╗ ██████╗██╗   ██╗██╗   ██╗██╗     ███╗   ██╗
  ██╔════╝██╔════╝██╔════╝██║   ██║██║   ██║██║     ████╗  ██║
  ███████╗█████╗  ██║     ██║   ██║██║   ██║██║     ██╔██╗ ██║
  ╚════██║██╔══╝  ██║     ╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║
  ███████║███████╗╚██████╗ ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║
  ╚══════╝╚══════╝ ╚═════╝  ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝
{Color.RESET}{Color.GREY}  AI-Driven Penetration Testing Agent | OSCP Methodology
  Author: SecVuln Project | For authorized use only
{Color.RESET}{Color.RED}  ⚠  Always obtain written permission before scanning!{Color.RESET}
"""


# =================================================================
# ENVIRONMENT & MODEL CONFIGURATION
# =================================================================
load_dotenv()
gh_token = os.getenv("GITHUB_TOKEN", "").strip()

# Validate that the API token is set before proceeding
if not gh_token:
    error("GITHUB_TOKEN is not set. Please configure your .env file.")
    sys.exit(1)

# Initialize the LLM engine using GitHub Models (OpenAI-compatible)
llm_engine = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=gh_token,
    base_url="https://models.inference.ai.azure.com"
)


# =================================================================
# STATE — Shared data passed between LangGraph nodes
# =================================================================
class SecurityState(TypedDict):
    target_ip: str        # The target host/IP provided by the user
    recon_payload: str    # Accumulated scan output (recon + NSE merged)
    security_analysis: str  # Final AI-generated penetration testing report


# =================================================================
# NODE 1 — RECONNAISSANCE ENGINE
# Runs nmap with fallback strategies until open ports are discovered.
# Strategy order: SYN → Full SYN → TCP Connect → Fragmented Packets
# =================================================================
def node_reconnaissance_engine(state: SecurityState) -> dict:
    target = state["target_ip"]
    section("NODE 1 — Reconnaissance Engine")
    info(f"Starting reconnaissance on target: {Color.BOLD}{target}{Color.RESET}")

    # Read nmap configuration from environment variables
    ports_env  = os.getenv("NMAP_PORTS", "--top-ports 1000")   # Default: top 1000 ports
    scan_type  = os.getenv("NMAP_SCAN_TYPE", "-sS")            # Default: SYN scan (stealthier)
    evasion    = os.getenv("NMAP_EVASION", "")                 # Optional evasion flags

    # Assemble the primary nmap command
    nmap_cmd = ["nmap", "-Pn", scan_type, "-sV", "-sC", "-T4", "--open", target]

    # Inject port range before the target argument
    nmap_cmd[-1:-1] = shlex.split(ports_env)

    # Inject optional evasion options before the target argument
    if evasion:
        nmap_cmd[-1:-1] = shlex.split(evasion)

    info(f"Running: {Color.GREY}{' '.join(nmap_cmd)}{Color.RESET}")
    start_time = time.time()

    try:
        result = subprocess.run(
            nmap_cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10-minute timeout for initial scan
        )

        if result.returncode != 0:
            # Non-zero return does not always mean total failure — attempt fallback
            warning(f"Initial scan returned non-zero exit code: {result.stderr.strip()}")
            scan_output = ""
        else:
            scan_output = result.stdout
            elapsed = round(time.time() - start_time, 2)
            success(f"Primary scan completed in {elapsed}s — {len(scan_output)} bytes received")

        # ── Fallback chain: escalate if no open ports were detected ──────────
        if "open" not in scan_output.lower():
            warning("No open ports detected. Escalating to full port SYN scan (-p-)...")

            # Fallback 1: Full port range SYN scan
            result_syn = subprocess.run(
                ["nmap", "-Pn", "-sS", "-sV", "-sC", "-T4", "-p-", "--min-rate=500", target],
                capture_output=True, text=True, timeout=600
            )
            scan_output = result_syn.stdout
            if "open" in scan_output.lower():
                success("Full SYN scan found open ports.")
            else:
                warning("Full SYN scan found nothing. Falling back to TCP connect scan...")

                # Fallback 2: TCP Connect scan (bypasses some firewall rules)
                result_tcp = subprocess.run(
                    ["nmap", "-Pn", "-sT", "-sV", "-sC", "-T4", "-p-", "--min-rate=500", target],
                    capture_output=True, text=True, timeout=600
                )
                scan_output = result_tcp.stdout
                if "open" in scan_output.lower():
                    success("TCP Connect scan found open ports.")
                else:
                    warning("TCP Connect failed. Attempting fragmented packet scan...")

                    # Fallback 3: Fragmented + MTU + Delay — maximum evasion mode
                    nmap_frag = [
                        "nmap",
                        "-Pn",                  # Disable host discovery (ICMP often blocked)
                        "-sS",                  # SYN scan (stealth)
                        "-f",                   # Fragment packets to evade DPI
                        "--mtu", "32",          # Force 32-byte MTU for deep fragmentation
                        "-sV",                  # Service version detection
                        "-sC",                  # Run default NSE scripts
                        "-T3",                  # Normal timing — reduces IDS fingerprinting
                        "--top-ports", "100",   # Limit ports to prevent timeout
                        "--scan-delay", "200ms",# Throttle to evade rate-based IDS
                        "--source-port", "53",  # Spoof DNS source port to bypass firewalls
                        "--data-length", "20",  # Append random payload bytes
                        target
                    ]
                    result_frag = subprocess.run(
                        nmap_frag, capture_output=True, text=True, timeout=600
                    )
                    scan_output = result_frag.stdout

                    if "open" in scan_output.lower():
                        success("Fragmented scan found open ports.")
                    else:
                        warning("All scan strategies exhausted. No open ports found.")

            success(f"Final scan output: {len(scan_output)} bytes")

        return {"recon_payload": scan_output}

    except FileNotFoundError:
        raise RuntimeError("nmap not found. Please install nmap and ensure it is in PATH.")
    except subprocess.TimeoutExpired:
        raise RuntimeError("nmap scan timed out after 600 seconds.")
    except Exception as e:
        raise RuntimeError(f"Reconnaissance failed unexpectedly: {e}")


# =================================================================
# NODE 2 — NSE VULNERABILITY SCANNER
# Runs targeted NSE scripts on ports found by Node 1.
# Scripts: vulners (CVE lookup), vuln (generic vuln check),
#          auth (auth bypass), default (basic enumeration)
# Skipped automatically if no open ports were found in recon.
# =================================================================
def node_vulnerability_scanner(state: SecurityState) -> dict:
    target     = state["target_ip"]
    recon_data = state["recon_payload"]

    section("NODE 2 — NSE Deep Vulnerability Scanner")

    if "open" not in recon_data.lower():
        warning("No open ports in recon data. Skipping NSE scan.")
        return {"recon_payload": recon_data}

    info(f"Open ports confirmed. Launching NSE scripts on: {Color.BOLD}{target}{Color.RESET}")

    # Run four NSE script categories for comprehensive vulnerability coverage
    nse_cmd = [
        "nmap", "-Pn", "-sV",
        "--script", "vulners,vuln,auth,default",  # CVE lookup + auth bypass + enumeration
        "-T4",
        target
    ]

    info(f"NSE command: {Color.GREY}{' '.join(nse_cmd)}{Color.RESET}")
    start_time = time.time()

    try:
        result = subprocess.run(nse_cmd, capture_output=True, text=True, timeout=600)
        nse_output = result.stdout
        elapsed = round(time.time() - start_time, 2)
        success(f"NSE Deep Scan completed in {elapsed}s")

        # Merge recon + NSE output into a single payload for the AI node
        combined_payload = (
            f"{recon_data}"
            f"\n\n{'─'*60}\n"
            f"--- NSE DEEP SCAN RESULTS ---\n"
            f"{'─'*60}\n"
            f"{nse_output}"
        )
        return {"recon_payload": combined_payload}

    except subprocess.TimeoutExpired:
        warning("NSE scan timed out. Continuing with recon data only.")
        return {"recon_payload": recon_data}
    except Exception as e:
        warning(f"NSE scan encountered an error: {e}. Continuing with recon data.")
        return {"recon_payload": recon_data}


# =================================================================
# NODE 3 — VULNERABILITY INTELLIGENCE (AI Analysis)
# Sends the combined scan payload to GPT-4o-mini with a detailed
# senior penetration tester system prompt. Produces the final report
# including CVEs, Metasploit paths, Searchsploit commands, and
# a prioritized attack plan.
# =================================================================
def node_vulnerability_intelligence(state: SecurityState) -> dict:
    section("NODE 3 — AI Vulnerability Intelligence")
    info("Transmitting scan data to AI engine for deep analysis...")

    system_instructions = SystemMessage(
        content=(
            "You are an elite penetration tester with 20 years of experience operating under OSCP methodology. "
            "When given Nmap scan results, you MUST:\n\n"
            "1. Identify EVERY open port and service with precise version details.\n"
            "2. Search your knowledge for ALL known CVEs for each service/version found.\n"
            "3. Rate each vulnerability clearly: CRITICAL / HIGH / MEDIUM / LOW.\n"
            "4. Provide EXACT Metasploit module paths (e.g., exploit/multi/handler).\n"
            "5. Provide EXACT Searchsploit commands for each vulnerability.\n"
            "6. Suggest detailed manual testing steps when no public exploit exists.\n"
            "7. If a service is unknown, analyze its behavior and suggest possible attack vectors.\n"
            "8. Identify any misconfigurations (open auth, weak ciphers, exposed admin panels).\n"
            "9. End with a clearly numbered, prioritized attack plan.\n\n"
            "Output format rules:\n"
            "- Use markdown headers for sections.\n"
            "- Use tables for services and CVEs where possible.\n"
            "- ONLY mention CVEs you are 100% certain exist for that exact version.\n"
            "- If unsure, state 'No confirmed CVEs — recommend manual testing' and elaborate.\n"
            "- Never refuse to answer — always provide the best possible analysis.\n"
            "- Be concise but thorough. Avoid generic filler text."
        )
    )

    user_payload = HumanMessage(
        content=(
            f"{'═'*60}\n"
            f"  SECVULN SCAN PAYLOAD — AWAITING ANALYSIS\n"
            f"{'═'*60}\n\n"
            f"{state['recon_payload']}\n\n"
            f"{'═'*60}\n"
            f"  END OF SCAN DATA\n"
            f"{'═'*60}"
        )
    )

    response = llm_engine.invoke([system_instructions, user_payload])
    success("AI analysis complete. Generating final report...")

    return {"security_analysis": response.content}


# =================================================================
# GRAPH — LangGraph 3-node stateful DAG
# Flow: Recon → NSE Scanner → AI Intelligence → END
# =================================================================
def compile_security_graph():
    system("Building SecVuln security analysis graph (3-node DAG)...")

    workflow = StateGraph(SecurityState)

    # Register the three processing nodes
    workflow.add_node("recon_node", node_reconnaissance_engine)
    workflow.add_node("nse_node",   node_vulnerability_scanner)
    workflow.add_node("intel_node", node_vulnerability_intelligence)

    # Define the linear execution order
    workflow.set_entry_point("recon_node")
    workflow.add_edge("recon_node", "nse_node")
    workflow.add_edge("nse_node",   "intel_node")
    workflow.add_edge("intel_node", END)

    system("Graph compiled successfully. Ready to execute.")
    return workflow.compile()


# =================================================================
# MAIN — Entry point for SecVuln
# Accepts target IP via CLI argument or interactive prompt.
# Validates input, compiles the graph, and runs the pipeline.
# =================================================================
if __name__ == "__main__":
    print(BANNER)

    # ── Resolve target IP ─────────────────────────────────────────
    if len(sys.argv) > 1:
        target_ip = sys.argv[1].strip()
    else:
        try:
            target_ip = input(
                f"{Color.CYAN}[?]{Color.RESET} Enter target IP or hostname: "
            ).strip()
        except KeyboardInterrupt:
            print()
            warning("Aborted by user.")
            sys.exit(0)

    if not target_ip:
        error("No target provided. Exiting.")
        sys.exit(1)

    # ── Validate input — allow IPs and valid hostnames only ───────
    if not re.match(r'^[\d\.]+$|^[a-zA-Z0-9\-\.]+$', target_ip):
        error(f"Invalid target format: '{target_ip}'. Exiting.")
        sys.exit(1)

    info(f"Target validated: {Color.BOLD}{Color.GREEN}{target_ip}{Color.RESET}")
    info(f"Pipeline: {Color.CYAN}Recon → NSE → AI Intelligence{Color.RESET}")

    # ── Build and execute the security pipeline ───────────────────
    security_agent = compile_security_graph()
    mission_data   = {"target_ip": target_ip, "recon_payload": "", "security_analysis": ""}

    try:
        final_output = security_agent.invoke(mission_data)

        # ── Print final report ────────────────────────────────────
        print(f"\n{Color.RED}{'═' * 60}{Color.RESET}")
        print(f"{Color.RED}{Color.BOLD}{'  SECVULN — AI PENETRATION TESTING REPORT':^60}{Color.RESET}")
        print(f"{Color.RED}{'═' * 60}{Color.RESET}\n")
        print(final_output["security_analysis"])
        print(f"\n{Color.GREY}{'─' * 60}{Color.RESET}")
        print(f"{Color.GREY}  SecVuln | For authorized testing only | Stay ethical.{Color.RESET}")
        print(f"{Color.GREY}{'─' * 60}{Color.RESET}\n")

    except KeyboardInterrupt:
        print()
        warning("Scan interrupted by user.")
        sys.exit(0)
    except Exception as error_msg:
        error(f"Pipeline failed: {error_msg}")
        sys.exit(1)