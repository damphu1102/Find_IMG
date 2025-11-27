import time
import random
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CẤU HÌNH ---
FOLDER_NAME = "hinh_anh_san_pham"
# Danh sách mẫu (Trong thực tế bạn sẽ đọc từ file Excel/TXT)
DANH_SACH_SP = [
    "iPhone 15 Pro Max 256GB",
    "Samsung Galaxy S24 Ultra",
    "Chuột Logitech G102",
    "Bàn phím cơ Keychron K2",
    "Tai nghe Sony WH-1000XM5"
]

def setup_driver():
    """Cấu hình Chrome Driver để tránh bị phát hiện là Bot"""
    chrome_options = Options()
    
    # Tạo thư mục profile riêng cho Selenium (tránh conflict với Chrome đang chạy)
    selenium_profile = os.path.join(os.getcwd(), "selenium_profile")
    if not os.path.exists(selenium_profile):
        os.makedirs(selenium_profile)
    
    chrome_options.add_argument(f"user-data-dir={selenium_profile}")
    
    # Chạy ẩn (không hiện trình duyệt) - Bỏ comment dòng dưới nếu muốn chạy ngầm
    # chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Loại bỏ dấu hiệu Automation
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def download_image(url, filename, folder):
    """Hàm tải ảnh từ URL và lưu vào folder"""
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            # Làm sạch tên file (bỏ các ký tự đặc biệt)
            valid_filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            file_path = os.path.join(folder, f"{valid_filename}.jpg")
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"[OK] Đã tải: {valid_filename}")
        else:
            print(f"[Lỗi] Không tải được ảnh: {filename}")
    except Exception as e:
        print(f"[Lỗi] Exception khi tải ảnh {filename}: {e}")

def main():
    print(">>> Đang khởi động Chrome với profile user...")
    driver = setup_driver()
    
    # Đợi Chrome mở xong (có thể mở các tab cũ)
    time.sleep(3)
    
    # Đóng tất cả tab cũ và mở tab mới
    print(f">>> Số tab đang mở: {len(driver.window_handles)}")
    
    # Giữ lại tab đầu tiên, đóng các tab khác
    if len(driver.window_handles) > 1:
        main_window = driver.window_handles[0]
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()
        driver.switch_to.window(main_window)
    
    # Bây giờ điều hướng đến Shopee
    print(">>> Đang truy cập Shopee...")
    driver.get("https://shopee.vn")
    time.sleep(5)
    
    print(f">>> URL hiện tại: {driver.current_url}")

    for ten_sp in DANH_SACH_SP:
        print(f"\n--- Đang tìm: {ten_sp} ---")
        
        try:
            # 1. Tạo URL tìm kiếm
            search_url = f"https://shopee.vn/search?keyword={ten_sp.replace(' ', '%20')}"
            print(f">>> Truy cập: {search_url}")
            driver.get(search_url)
            
            # 2. Random delay (QUAN TRỌNG: để tránh bị chặn)
            delay = random.uniform(5, 8)
            print(f">>> Đợi {delay:.1f}s để trang load...")
            time.sleep(delay)
            
            # 3. Kiểm tra URL hiện tại (có thể bị redirect về login)
            current_url = driver.current_url
            if "login" in current_url:
                print("[Cảnh báo] Shopee yêu cầu đăng nhập! Vui lòng đăng nhập thủ công trong trình duyệt.")
                print(">>> Đợi 30s để bạn đăng nhập...")
                time.sleep(30)
                driver.get(search_url)
                time.sleep(5)
            
            # 4. Thử nhiều selector khác nhau (Shopee hay thay đổi)
            selectors = [
                '//img[contains(@class, "shopee-search-item-result__image")]',
                '//div[@data-sqe="item"]//img',
                '//a[@data-sqe="link"]//img',
                '//div[contains(@class, "col-xs-2-4")]//img',
                '//img[contains(@src, "vn-11134207")]'  # CDN của Shopee
            ]
            
            elements = []
            for selector in selectors:
                try:
                    print(f">>> Thử selector: {selector[:50]}...")
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements:
                        print(f">>> Tìm thấy {len(elements)} ảnh!")
                        break
                except:
                    continue
            
            if elements:
                # Lấy ảnh đầu tiên
                img_url = elements[0].get_attribute("src")
                
                # Nếu không có src, thử data-src (lazy load)
                if not img_url or "placeholder" in img_url:
                    img_url = elements[0].get_attribute("data-src")
                
                if img_url and "http" in img_url:
                    download_image(img_url, ten_sp, FOLDER_NAME)
                else:
                    print(f"[Bỏ qua] Link ảnh không hợp lệ: {img_url}")
            else:
                print(f"[Bỏ qua] Không tìm thấy sản phẩm nào cho {ten_sp}")
                # Lưu screenshot để debug
                screenshot_path = f"debug_{ten_sp[:20]}.png"
                driver.save_screenshot(screenshot_path)
                print(f">>> Đã lưu screenshot: {screenshot_path}")

        except Exception as e:
            print(f"[Lỗi] Có vấn đề khi xử lý {ten_sp}: {e}")
            # Lưu screenshot khi lỗi
            try:
                driver.save_screenshot(f"error_{ten_sp[:20]}.png")
            except:
                pass
    
    print(">>> Hoàn tất! Đóng trình duyệt.")
    driver.quit()

if __name__ == "__main__":
    main()