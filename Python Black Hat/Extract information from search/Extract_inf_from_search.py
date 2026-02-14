from playwright.sync_api import sync_playwright

def extract(query):
    with sync_playwright() as pr:
        browser = pr.chromium.launch(headless=False)
        page = browser.new_page()
        url_search = f"http://www.bing.com/search?q={query}"
        page.goto(url_search)
        num_pages = 5  #Number of pages we need to move in
        for pago in range(1,num_pages+1):
            try:
                page.wait_for_selector("li.b_algo a")
                # <li><a href="nextpahe.html">1</li>
                # <li><a href="nextpahe.html">2</li>
                # <li><a href="nextpahe.html">3</li>
                # <li><a href="nextpahe.html">4</li>
                # <li><a href="nextpahe.html">5</li>
                links = page.eval_on_selector_all("li.b_algo a", "element => element.map(el => el.href)")
                for leo in links:
                    print(leo)
                next_page = page.query_selector("a.sb_pagN")
                if next_page:
                    next_page.click()
                    page.wait_for_timeout(5000)
                    
                else:
                    break
            except:
                print("Captcha Block Founded! Or the result has finished")   
                break   
        browser.close()


extract("index.php?id=1")