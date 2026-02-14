from playwright.sync_api import sync_playwright

def osint_ex(query):
    with sync_playwright() as pr:
        browser = pr.chromium.launch(headless=False)
        
            
        page = browser.new_page()
        search_link = f"https://www.bing.com/search?q={query}"
        page.goto(search_link)
        num_pages = 6
        all_result = []
        for page_num in range(1,num_pages+1):
            print(f"Extract Urls From Pages :{page_num}")
            page.wait_for_selector("li.b_algo")
            results = page.query_selector_all("li.b_algo")
            for result in results:
                try:
                    title = result.query_selector("a").inner_text()
                    link = result.query_selector("a").get_attribute("href")
                    all_result.append({"title": title, "link": link})
                    print(f"Title: {title}\nLink: {link}\n")
                except:
                    pass
            next_page_button = page.query_selector("a.sb_pagN")
            if next_page_button:
                next_page_button.click()
                page.wait_for_timeout(3000)
            else:
                break

        browser.close()
        print("All Result: ")
        for result in all_result:
            print(f"Title: {result['title']}\nLink: {result['link']}\n")


osint_ex("Mohamed")
