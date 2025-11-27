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
    
    # Bây giờ điều hướng đến Google Images
    print(">>> Đang truy cập Google Images...")
    driver.get("https://www.google.com/imghp?hl=vi")
    time.sleep(3)
    
    print(f">>> URL hiện tại: {driver.current_url}")

    for ten_sp in DANH_SACH_SP:
        print(f"\n--- Đang tìm: {ten_sp} ---")
        
        try:
            # 1. Tạo URL tìm kiếm Google Images
            search_url = f"https://www.google.com/search?q={ten_sp.replace(' ', '+')}&tbm=isch&hl=vi"
            print(f">>> Truy cập: {search_url}")
            driver.get(search_url)
            
            # 2. Random delay (QUAN TRỌNG: để tránh bị chặn)
            delay = random.uniform(3, 5)
            print(f">>> Đợi {delay:.1f}s để trang load...")
            time.sleep(delay)
            
            # 3. Tìm ảnh có thể click được
            print(">>> Tìm ảnh trong kết quả...")
            
            # Thử nhiều selector khác nhau cho Google Images
            thumbnail_selectors = [
                '//img[@class="rg_i Q4LuWd"]',
                '//div[@jsname]//img',
                '//img[contains(@src, "gstatic")]',
                '//h3//ancestor::div[2]//img'
            ]
            
            thumbnail = None
            for selector in thumbnail_selectors:
                try:
                    print(f">>> Thử selector: {selector[:40]}...")
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    thumbnails = driver.find_elements(By.XPATH, selector)
                    
                    # Tìm ảnh đầu tiên có thể click được
                    for thumb in thumbnails[:10]:  # Chỉ thử 10 ảnh đầu
                        try:
                            if thumb.is_displayed() and thumb.size['width'] > 50:
                                thumbnail = thumb
                                print(f">>> Tìm thấy ảnh có thể click!")
                                break
                        except:
                            continue
                    
                    if thumbnail:
                        break
                except:
                    continue
            
            if not thumbnail:
                raise Exception("Không tìm thấy ảnh có thể click")
            
            # 4. Click vào ảnh bằng JavaScript (tránh lỗi element not interactable)
            print(">>> Click vào ảnh để xem full size...")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", thumbnail)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", thumbnail)
            time.sleep(3)
            
            # 5. Lấy ảnh full size từ panel bên phải
            # Sau khi click, Google hiển thị ảnh lớn hơn
            print(">>> Đang tìm ảnh full size...")
            
            # Tìm tất cả ảnh trên trang và lấy ảnh lớn nhất
            all_images = driver.find_elements(By.TAG_NAME, "img")
            
            img_url = None
            max_size = 0
            
            for img in all_images:
                try:
                    src = img.get_attribute("src")
                    if not src or "data:image" in src or "gstatic" in src:
                        continue
                    
                    # Lấy kích thước ảnh
                    width = img.size.get('width', 0)
                    height = img.size.get('height', 0)
                    size = width * height
                    
                    if size > max_size and "http" in src:
                        max_size = size
                        img_url = src
                        print(f">>> Tìm thấy ảnh {width}x{height}px")
                except:
                    continue
            
            # 6. Nếu không tìm thấy, thử lấy từ thumbnail
            if not img_url:
                print(">>> Không lấy được ảnh full, dùng thumbnail...")
                img_url = thumbnail.get_attribute("src")
            
            # 7. Download ảnh
            if img_url and "http" in img_url:
                download_image(img_url, ten_sp, FOLDER_NAME)
            else:
                print(f"[Bỏ qua] Link ảnh không hợp lệ: {img_url}")
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