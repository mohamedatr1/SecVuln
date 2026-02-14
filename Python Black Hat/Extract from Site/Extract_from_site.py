from playwright.sync_api import sync_playwright
import re
with sync_playwright() as pr:
    browser = pr.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://testphp.vulnweb.com/")
    print("Page Title: " , page.inner_text("body"))
    print("Code HTML: ", page.inner_html("body"))
    
    # <a href= "google.com">google</a>  # EXMPL ABT JS CODE
    links = page.eval_on_selector_all("a",  "elements => elements.map(el => el.href)") #bring links from (JS Code)
      
    for link in links:
        print("Link: ",link)
    
    meta_one = page.query_selector("meta[http-equiv='Content-Type']")
    if meta_one:
        print("Meta One: ", meta_one.get_attribute("content"))

    #EMAILS: 

    full_text = page.inner_text("body")        #This is so important to find emails
    # mohamed31%DSA@gmail.-com       # EXMPL FOR EMAIL 
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}", full_text)   
    print("Emails: ",emails)
    #NUMBERS:
    # page.goto("https://quackr.io/j")
    
    phones = re.findall(r"\+?\d[\d\s()-]{7,}",full_text)
    print("Numbers: ",phones)
    
    #<img src='www.google.com'/image1.jpg>  # EXMPL ABT JS CODE
    images = page.eval_on_selector_all("img","imgs => imgs.map(img => img.src)")
    print("Images: ",images)

    browser.close()