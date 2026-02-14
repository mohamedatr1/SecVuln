Web Directory & Path Discoverer
Description
This script is a specialized fuzzer designed to identify hidden directories and files on a web server. By automating the process of testing a list of potential paths, it helps security researchers map out the structure of a target website and find sensitive locations.

Technical Steps
File Handling: Opens and reads a local wordlist (path.txt) containing common directory and file names.

URL Construction: Dynamically builds full target URLs by combining the base domain with each path from the list.

HTTP Requests: Uses the requests library to send GET requests for every generated URL.

Status Analysis:

200 OK: Confirms the resource exists and is accessible.

404 Not Found: Confirms the resource does not exist.

Other Statuses: Captures different responses (like 403 Forbidden or 500 Error) for further investigation.

Data Cleaning: Implements .strip() to ensure no newline characters break the URL format.

Requirements
requests library.

A wordlist file named path.txt.