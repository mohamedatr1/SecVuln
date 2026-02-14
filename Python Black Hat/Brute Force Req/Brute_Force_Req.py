from playwright.sync_api import sync_playwright

url = "http://testphp.vulnweb.com/login.php"
with sync_playwright() as pr:
    browser = pr.chromium.launch(headless=False)
    context = browser.new_context(
        record_video_dir="videos"
    )
    page = context.new_page()
    page.goto(url)
    page.fill("input[name='uname']","test")
    page.fill("input[name='pass']","test")
    page.click("input[type='submit']")
    page.wait_for_timeout(5000)
    page.close()
    
    video = page.video
    video_path = "videos/test.mp4"
    video.save_as(video_path)


    browser.close()
