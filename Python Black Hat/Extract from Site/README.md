# Web Data & OSINT Scraper

### Description
This script is an automated data extraction tool designed to crawl websites and scrape essential information for OSINT (Open Source Intelligence). By utilizing a headless browser, it renders JavaScript-heavy content to capture data that traditional static scrapers often miss.



### Technical Workflow
* **Headless Browser Execution**: Launches a Chromium instance in the background for fast and efficient DOM parsing.
* **Dynamic Link Extraction**: Executes JavaScript directly within the browser context using `eval_on_selector_all` to gather all hyperlink (`<a>` tag) destinations from the memory.
* **Pattern Matching (Regex)**:
    * **Email Harvesting**: Scans the rendered page text for email addresses using a complex regular expression pattern.
    * **Contact Identification**: Detects phone numbers and numerical contact strings using specific digit-based patterns.
* **Metadata Inspection**: Queries the page for specific meta-tags (like Content-Type) to identify site encoding and technology.
* **Media Scraping**: Programmatically identifies all image source URLs (`<img>` tags) present on the page.



### Requirements
* **Playwright**: For browser automation and dynamic content rendering.
* **re**: (Standard library) For advanced regular expression pattern matching.

### Installation
```bash
pip install playwright
playwright install chromium
