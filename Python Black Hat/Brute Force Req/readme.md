# Web Login Automation & Video Recorder

### Description
This script is a specialized automation tool designed to interact with web authentication forms and document the process. It is used for automated testing and creating video evidence for security proof-of-concepts (PoC).

### Technical Workflow
* **Headless Browser Control**: Launches a Chromium instance in visible mode (`headless=False`) to monitor interactions in real-time.
* **Session Recording**: Initializes a browser context configured to capture all screen activity and save it to a designated `videos` directory.
* **Automated Navigation**: Directs the browser to the target authentication endpoint.
* **Field Manipulation**: Automatically identifies and populates the `uname` and `pass` input fields with specified credentials.
* **Form Submission**: Executes a programmatic click on the submit button to initiate the login sequence.
* **Persistence**: Includes a 5-second buffer (`wait_for_timeout`) to ensure post-login pages or redirects are fully captured.
* **Video Export**: Finalizes the recording and saves the resulting MP4 file to a defined local path.



### Requirements
* **Playwright**: For browser automation and session control.
* **Chromium**: The underlying browser engine used for the execution.

### Installation
```bash
pip install playwright
playwright install chromium
