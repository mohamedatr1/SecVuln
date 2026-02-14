# Domain WHOIS Intelligence Extractor

### Description
[cite_start]This script is a reconnaissance tool used to retrieve registration and ownership details for a specific domain or IP address[cite: 3]. [cite_start]It is a fundamental component of the "Information Gathering" phase in security auditing and network analysis[cite: 3].

### Technical Workflow
* [cite_start]**Target Definition**: Takes a specific IP address or domain name as input for analysis[cite: 3].
* [cite_start]**WHOIS Protocol Query**: Utilizes the `python-whois` library to perform lookups against global WHOIS databases[cite: 2, 3].
* **Intelligence Gathering**: Extracts critical administrative and technical data, including:
    * [cite_start]**Registrar Information**: Details about the entity that registered the domain[cite: 3].
    * [cite_start]**Lifecycle Dates**: Registration and expiration dates of the domain[cite: 3].
    * [cite_start]**DNS Infrastructure**: Identification of active Name Servers[cite: 3].
    * [cite_start]**Contact Data**: Publicly available contact details for the organization or owner[cite: 3].
* [cite_start]**Console Output**: Prints the structured raw data for immediate analysis[cite: 3].



### Requirements
* [cite_start]**python-whois**: The primary library for querying WHOIS servers[cite: 3].

### Installation
```bash
pip install python-whois
