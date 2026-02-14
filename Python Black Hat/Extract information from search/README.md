Bing Search OSINT Automator
Description
This script is an automated reconnaissance tool designed to scrape search results from Bing for specific queries (Google Dorks). It automates the process of navigating through multiple search pages to collect URLs, which is essential for large-scale security auditing and vulnerability research.

Technical Steps
Automated Search: Constructively builds a Bing search URL using a custom query (e.g., SQLi dorks like index.php?id=1).

Dynamic Content Rendering: Uses Playwright to handle the search engine's interface and wait for specific CSS selectors (li.b_algo).

Multi-page Navigation (Pagination): Implements a loop to scrape up to 5 consecutive search pages automatically.

Link Extraction: Executes a JavaScript snippet within the browser context to gather all result links from the current page efficiently.

Human-like Interaction: Uses wait_for_timeout and automated clicks on the "Next Page" button to mimic human browsing and reduce the risk of being blocked.

Error Handling: Includes a try-except block to detect Captcha challenges or the end of search results gracefully.

Requirements
playwright library.

Chromium browser (installed via Playwright).