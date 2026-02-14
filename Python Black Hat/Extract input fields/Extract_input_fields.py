from playwright.sync_api import sync_playwright

url = "http://testphp.vulnweb.com/login.php"
with sync_playwright() as pr:
    browser = pr.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    forms = page.query_selector_all("form")
    for form in forms:
        print("form: ",form.inner_html())
 

    browser.close()
