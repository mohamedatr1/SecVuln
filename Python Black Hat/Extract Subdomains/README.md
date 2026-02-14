Multi-Threaded Subdomain Brute-Forcer
Description
This is a high-performance reconnaissance tool designed to discover subdomains by testing all possible character combinations. It features a recursive generation engine and utilizes multi-threading to achieve high-speed scanning, making it significantly faster than sequential scripts.

Technical Steps
Recursive Generation: Uses a recursive algorithm to generate every possible combination of letters (a-z) up to a defined length (e.g., aaa, aab, aac...).

Concurrent Execution (Threading): Employs ThreadPoolExecutor to run multiple network checks simultaneously (up to 10 threads). This prevents the script from waiting for one URL to respond before checking the next.

HTTP Validation: Sends requests to each generated subdomain and filters results based on HTTP status codes (200, 301, 302).

Resilience: Implements a 3-second timeout and exception handling to ensure the script continues running even if a connection fails or hangs.

Requirements
requests library.

concurrent.futures .