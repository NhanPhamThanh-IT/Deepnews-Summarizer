from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_cnn_articles():
    # Cấu hình Chrome cho headless mode
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Khởi tạo WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL trang CNN cần scrap
    url = "https://edition.cnn.com/us"  # Đổi URL nếu cần
    driver.get(url)
    time.sleep(3)  # Chờ tải trang

    articles = []

    # Tìm tất cả thẻ <a> có class như bạn yêu cầu
    anchor_tags = driver.find_elements(By.CSS_SELECTOR, 'a.container__link.container__link--type-article.container_lead-plus-headlines__link')

    for a in anchor_tags:
        try:
            # Lấy các thuộc tính cần thiết từ thẻ <a>
            href = a.get_attribute("href")
            
            # Tìm tiêu đề từ thẻ <span class="container__headline-text">
            title = a.find_element(By.CLASS_NAME, "container__headline-text").text.strip()

            # Lưu kết quả
            articles.append({
                "title": title,
                "url": href
            })
        except Exception as e:
            print(f"Skipped one item due to: {e}")
            continue

    driver.quit()  # Đóng driver sau khi xong
    return articles
