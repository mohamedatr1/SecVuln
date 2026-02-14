Description:
This script automates the login process for a web application and records the entire session as an MP4 video. It is designed for automated testing and creating video evidence for security proof-of-concepts (PoC).

Technical Steps

Launch Browser: Opens a Chromium browser in visible mode (headless=False).


Video Setup: Creates a browser context configured to record all interactions and save them to a "videos" directory.


Navigation: Directs the browser to the specified login URL.


Form Interaction: Automatically locates and fills the "uname" and "pass" input fields.


Submission: Triggers a click on the submit button to process the login.


Persistence: Waits for 5 seconds to ensure the post-login page loads completely.


Export: Closes the page and saves the generated video to the local path "videos/test.mp4".

Requirements
Playwright library.

Chromium browser binaries.

Usage

Run the script to execute the login. A video file will be generated in the project folder under videos/test.mp4.
