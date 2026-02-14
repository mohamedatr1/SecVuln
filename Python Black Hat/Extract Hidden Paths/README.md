# Web Directory & Path Discoverer

### Description
This script is a specialized fuzzer designed to identify hidden directories and files on a web server. By automating the process of testing a list of potential paths, it helps security researchers map out the structure of a target website and uncover sensitive locations.



### Technical Workflow
* **File Handling**: Opens and reads a local wordlist (`path.txt`) containing common directory and file names.
* **URL Construction**: Dynamically builds full target URLs by combining the base domain with each path provided in the list.
* **HTTP Requests**: Utilizes the `requests` library to send GET requests for every generated URL.
* **Status Analysis**:
    * **200 OK**: Confirms the resource exists and is accessible.
    * **404 Not Found**: Confirms the resource does not exist.
    * **Other Statuses**: Captures different responses (such as 403 Forbidden or 500 Server Error) for further investigation.
* **Data Cleaning**: Implements the `.strip()` method to ensure no newline characters or trailing spaces interfere with the URL format.

### Requirements
* **Requests**: The primary library for handling HTTP communications.
* **Wordlist**: A text file (e.g., `path.txt`) containing the directory names to test.

### Installation
```bash
pip install requests
