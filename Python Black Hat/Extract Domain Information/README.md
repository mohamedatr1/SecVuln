# Domain WHOIS Intelligence Extractor

### Description
This script is a reconnaissance tool used to retrieve registration and ownership details for a specific domain or IP address. It is a fundamental component of the "Information Gathering" phase in security auditing and network analysis.

### Technical Workflow
* **Target Definition**: Takes a specific IP address or domain name as input for analysis.
* **WHOIS Protocol Query**: Utilizes the `python-whois` library to perform lookups against global WHOIS databases.
* **Intelligence Gathering**: Extracts critical administrative and technical data, including:
    * **Registrar Information**: Details about the entity that registered the domain.
    * **Lifecycle Dates**: Registration and expiration dates of the domain
    * **DNS Infrastructure**: Identification of active Name Servers
  * **Contact Data**: Publicly available contact details for the organization or owner.
* **Console Output**: Prints the structured raw data for immediate analysis.



### Requirements
* **python-whois**: The primary library for querying WHOIS servers.

### Installation
```bash
pip install python-whois

