OSINT Search & Result Aggregator
Description
This script is an advanced OSINT (Open Source Intelligence) tool designed to automate search queries on Bing and aggregate results into a structured format. Unlike basic scrapers, it navigates through multiple pages, extracts both titles and URLs, and stores them in a list for further analysis or data export.

Technical Steps
Targeted Search: Initiates a search session using a specific query (e.g., a person's name or a specific domain).

Dynamic Selector Handling: Uses wait_for_selector to ensure that search results (li.b_algo) are fully rendered before extraction, preventing script crashes.

Structured Data Extraction:

Locates the title within the anchor <a> tag.

Extracts the exact href attribute to get the destination link.

Data Aggregation: Appends each result as a dictionary (Title/Link) into a master list (all_result), demonstrating solid data management.

Automated Pagination: Checks for the existence of the "Next" button (a.sb_pagN) and clicks it to move through up to 6 pages of results.

Error Resiliency: Implements a try-except block within the loop to skip broken or incomplete search result elements without stopping the entire process.

Requirements
playwright library.

Chromium browser.