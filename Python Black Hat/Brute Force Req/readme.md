# Web Login Automation & Video Recorder

### Description
This script is a specialized automation tool designed to interact with web authentication forms and document the process. [cite_start]It is used for automated testing and creating video evidence for security proof-of-concepts (PoC)[cite: 15, 16].

### Technical Workflow
* [cite_start]**Headless Browser Control**: Launches a Chromium instance in visible mode (`headless=False`) to monitor interactions in real-time[cite: 1, 15].
* [cite_start]**Session Recording**: Initializes a browser context configured to capture all screen activity and save it to a designated `videos` directory[cite: 1, 15].
* [cite_start]**Automated Navigation**: Directs the browser to the target authentication endpoint[cite: 1, 15].
* [cite_start]**Field Manipulation**: Automatically identifies and populates the `uname` and `pass` input fields with specified credentials[cite: 1, 15].
* [cite_start]**Form Submission**: Executes a programmatic click on the submit button to initiate the login sequence[cite: 1, 15].
* [cite_start]**Persistence**: Includes a 5-second buffer (`wait_for_timeout`) to ensure post-login pages or redirects are fully captured[cite: 1, 15].
* [cite_start]**Video Export**: Finalizes the recording and saves the resulting MP4 file to a defined local path[cite: 1, 15].



### Requirements
* [cite_start]**Playwright**: For browser automation and session control[cite: 1, 16].
* [cite_start]**Chromium**: The underlying browser engine used for the execution[cite: 1, 16].

### Installation
```bash
pip install playwright
playwright install chromium
