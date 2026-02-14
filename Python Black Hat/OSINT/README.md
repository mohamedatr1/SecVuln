# OSINT Search & Result Aggregator

### Description
This script is an advanced OSINT (Open Source Intelligence) tool designed to automate search queries on Bing and aggregate results into a structured data format. It handles complex tasks such as multi-page navigation, metadata extraction, and persistent data storage within the session.



### Technical Workflow
* **Automated Search Execution**: Initiates a headless or headed browser session to perform targeted searches based on user-defined queries (e.g., specific names, entities, or domains).
* **Dynamic Content Synchronization**: Utilizes `wait_for_selector` to ensure that the search engine's results (`li.b_algo`) are fully rendered and accessible before attempting data extraction.
* **Structured Data Extraction**: 
    * **Title Capture**: Programmatically identifies the anchor `<a>` tag to extract the descriptive text of the search result.
    * **Link Retrieval**: Fetches the exact `href` attribute to obtain the direct destination URL.
* **Data Aggregation**: Appends each discovered result into a centralized list of dictionaries (`all_result`). This structured approach allows for easy integration with databases or export to JSON/CSV formats.
* **Intelligent Pagination**: Detects the existence of the "Next Page" navigation element (`a.sb_pagN`) and executes a click event to iterate through up to 6 pages of search results automatically.
* **Failure Tolerance**: Employs internal `try-except` blocks to ensure the script continues processing even if individual result elements are malformed or blocked.

### Requirements
* **Playwright**: For high-level browser automation and DOM manipulation.
* **Chromium**: The browser engine used to interact with the search engine.

### Installation
```bash
pip install playwright
playwright install chromium
