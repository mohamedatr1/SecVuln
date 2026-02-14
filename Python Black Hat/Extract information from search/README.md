# Bing Search OSINT Automator

### Description
This script is an automated reconnaissance tool designed to scrape search results from Bing for specific queries (Google Dorks). It automates the process of navigating through multiple search pages to collect URLs, which is essential for large-scale security auditing and vulnerability research.



### Technical Workflow
* **Automated Search Querying**: Constructively builds a Bing search URL using custom dorks (e.g., `index.php?id=1`) to identify potentially vulnerable web targets.
* **Dynamic Content Handling**: Uses Playwright to manage the search engine's interface and utilizes `wait_for_selector` to ensure elements like `li.b_algo` are fully loaded before interaction.
* **Multi-page Navigation (Pagination)**: Implements a logical loop to automatically scrape up to 5 consecutive search pages.
* **JavaScript Link Extraction**: Executes a JavaScript snippet within the browser context using `eval_on_selector_all` to efficiently gather all hyperlink (`<a>` tags) URLs from the search results.
* **Human-like Interaction**: Mimics human browsing behavior by using `wait_for_timeout` and automated clicks on the "Next Page" button (`a.sb_pagN`) to minimize the risk of being flagged as a bot.
* **Error & Anti-Bot Handling**: Includes a `try-except` block to gracefully detect and handle Captcha challenges or the natural end of search results without crashing.

### Requirements
* **Playwright**: For browser automation and session control.
* **Chromium**: The browser engine used to perform the searches.

### Installation
```bash
pip install playwright
playwright install chromium
