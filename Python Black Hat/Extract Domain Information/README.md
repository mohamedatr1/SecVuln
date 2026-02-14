Domain WHOIS Intelligence Extractor
Description
This script is a reconnaissance tool used to retrieve registration and ownership details for a specific domain or IP address. It is an essential part of the Information Gathering phase in security auditing.

Technical Steps
Input: Takes a domain name or an IP address as a target.

WHOIS Query: Uses the whois library to query global WHOIS databases.

Data Retrieval: Extracts critical information such as:

Domain registrar and registration date.

Expiration date.

Name servers (DNS).

Owner/Organization contact details (if public).

Output: Prints the raw and structured intelligence data to the console for analysis.

Requirements
python-whois library.