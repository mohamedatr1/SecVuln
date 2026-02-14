Web Data & OSINT Scraper
Description
This script is an automated data extraction tool designed to crawl a website and scrape essential information for OSINT (Open Source Intelligence). It uses a headless browser to render JavaScript and extract hidden data that traditional scrapers might miss.

Technical Steps
Headless Browser Launch: Starts a Chromium instance in the background for fast execution.

DOM Analysis: Retrieves the page title and full HTML content of the body.

Dynamic Link Extraction: Uses JavaScript execution (eval_on_selector_all) to grab all hyperlinks (<a> tags) directly from the browser's memory.

Metadata Inspection: Queries specific meta tags to identify the website's content type and encoding.

Pattern Matching (Regex):

Scans the visible text for email addresses using complex regular expressions.

Identifies phone numbers and contact digits across the page.

Media Scraping: Collects all image source URLs (<img> tags) found on the page.

Requirements
playwright

re (Python built-in)