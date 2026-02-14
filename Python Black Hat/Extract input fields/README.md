Web Form Inspector & Parser
Description
This script is a specialized web auditing tool designed to detect and extract HTML forms from a webpage. It is used to map out the "Attack Surface" of a website by identifying where user input is accepted, which is the first step in testing for vulnerabilities like SQL Injection or XSS.

Technical Steps
Headless Browser Execution: Launches a Chromium instance in the background for efficient DOM parsing.

Page Navigation: Directs the browser to the target URL to load all static and dynamic elements.

Form Discovery: Uses query_selector_all("form") to locate every <form> tag within the page structure.

HTML Extraction: Iterates through each found form and extracts its internal HTML code (inner_html), revealing input names, types, and action endpoints.

Clean Up: Closes the browser instance to free up system resources.

Requirements
playwright library.

Chromium browser binaries.