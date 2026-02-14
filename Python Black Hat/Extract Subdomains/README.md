# Multi-Threaded Subdomain Brute-Forcer

### Description
This high-performance reconnaissance tool is designed to discover subdomains by testing all possible character combinations. It features a recursive generation engine and utilizes multi-threading to achieve high-speed scanning, making it significantly more efficient than sequential scripts.



### Technical Workflow
* **Recursive Generation**: Uses a recursive algorithm to generate every possible combination of lowercase letters (a-z) up to a user-defined length (e.g., 'a', 'ab', 'abc').
* **Concurrent Execution**: Employs the `ThreadPoolExecutor` from the `concurrent.futures` module to manage 10 simultaneous worker threads. This allows the script to handle multiple network requests in parallel.
* **HTTP Validation**: Sends GET requests to each generated subdomain and filters the results based on standard success and redirect status codes (200, 301, 302).
* **Error Resilience**: Implements a 3-second timeout and robust exception handling to ensure that failed connections or DNS timeouts do not interrupt the scanning process.
* **Dynamic Mapping**: Uses the `.map()` function to distribute the list of generated subdomains across the available thread pool for optimal resource utilization.

### Requirements
* **Requests**: For handling HTTP communication and status code validation.
* **Concurrent.futures**: (Standard library) For managing the thread pool.

### Installation
```bash
pip install requests
