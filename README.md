# Hệ thống Tự động Tải Hình Ảnh Sản Phẩm

Công cụ tự động tìm kiếm và tải hình ảnh sản phẩm từ Google Images dựa trên danh sách trong file Excel.

## Tính năng

- ✅ Đọc danh sách sản phẩm từ file Excel (DSSP.xlsx)
- ✅ **Tìm kiếm thông minh**: Kết hợp barcode + tên sản phẩm để tăng độ chính xác
- ✅ **Tự động chọn ảnh kế tiếp**: Nếu không tải được ảnh, tự động thử ảnh tiếp theo
- ✅ **Luôn cố gắng lấy đủ 3 ảnh**: Lặp qua tối đa 15 ảnh để tìm 3 ảnh tốt
- ✅ **Multi-threading**: Chạy 3 browser song song (tăng tốc 3x)
- ✅ **Thread-safe Excel writing**: Tránh corrupt file khi ghi đồng thời
- ✅ Click vào ảnh để lấy phiên bản full size (chất lượng cao)
- ✅ Tải ảnh về thư mục `hinh_anh_san_pham`
- ✅ Tự động ghi tên file ảnh vào Excel (3 cột riêng biệt)
- ✅ Tên file không dấu, thay khoảng trắng bằng `_`
- ✅ Profile riêng cho mỗi thread để tránh xung đột
- ✅ Anti-detection (tránh bị phát hiện là bot)
- ✅ Progress tracking (hiển thị tiến độ)

## Yêu cầu hệ thống

- Python 3.7+
- Google Chrome
- Windows/Linux/MacOS

## Cài đặt

### 1. Clone hoặc tải project

```bash
git clone <repository-url>
cd Find_IMG
```

### 2. Cài đặt thư viện

```bash
pip install selenium webdriver-manager requests openpyxl
```

## Cấu trúc file

```
Find_IMG/
├── find.py              # Script chính
├── DSSP.xlsx            # File Excel chứa danh sách sản phẩm
├── README.md            # Hướng dẫn sử dụng
├── .gitignore           # Loại trừ file không cần thiết
├── hinh_anh_san_pham/   # Thư mục chứa ảnh đã tải (tự động tạo)
└── selenium_profile/    # Chrome profile (tự động tạo)
```

## Cách sử dụng

### 1. Chuẩn bị file Excel

Mở file `DSSP.xlsx` và nhập danh sách sản phẩm vào **cột A (barcode)** và **cột B (name)** (từ dòng 2 trở đi):

| Barcode      | Tên sản phẩm                  | Ảnh 1            | Ảnh 2            | Ảnh 3            |
| ------------ | ----------------------------- | ---------------- | ---------------- | ---------------- |
| 8850006325636 | KDR Colgate TOT ActiveFresh 150g | _(tự động điền)_ | _(tự động điền)_ | _(tự động điền)_ |
| 8850006332030 | BCDR Colgate 360 Char Spiral 2   | _(tự động điền)_ | _(tự động điền)_ | _(tự động điền)_ |

**Lưu ý quan trọng:**
- ⚠️ **Đóng file Excel trước khi chạy script** để tránh lỗi ghi file
- Script sẽ tìm kiếm theo **barcode + tên sản phẩm** (cột A + cột B) để tăng độ chính xác
- Tên file ảnh sẽ dựa trên **name** (cột B)

### 2. Chạy script

```bash
python find.py
```

### 3. Theo dõi quá trình

Script sẽ:

1. Khởi động **3 Chrome instances** song song (mỗi cái có profile riêng)
2. Truy cập Google Images
3. Tìm kiếm từng sản phẩm theo **barcode + tên sản phẩm** (cột A + cột B)
4. Tìm tối đa **15 ảnh** trong kết quả
5. **Tự động chọn ảnh kế tiếp** nếu không tải được ảnh hiện tại
6. Lặp cho đến khi lấy đủ **3 ảnh** hoặc hết ảnh để thử
7. Tải ảnh về thư mục `hinh_anh_san_pham` với số thứ tự (_1, _2, _3)
8. Ghi tên file vào cột C, D, E của Excel (thread-safe)
9. Hiển thị progress: "X/Y sản phẩm hoàn thành"

**Bạn sẽ thấy:**
- 3 cửa sổ Chrome mở cùng lúc
- Mỗi cửa sổ xử lý một sản phẩm khác nhau
- Log hiển thị `[Worker 0]`, `[Worker 1]`, `[Worker 2]`
- Tìm kiếm kết hợp: "8850006325636 KDR Colgate TOT ActiveFresh 150g"
- Log chi tiết: "✓ Đã tải ảnh 1/3", "✗ Không tải được, thử ảnh tiếp theo..."

### 4. Kết quả

- **Ảnh đã tải**: Lưu trong thư mục `hinh_anh_san_pham/`
- **Tên file**: Không dấu, dấu cách thay bằng `_`, có số thứ tự
  - Ví dụ: 
    - `Colgate_Active_Fresh_150g_1.jpg`
    - `Colgate_Active_Fresh_150g_2.jpg`
    - `Colgate_Active_Fresh_150g_3.jpg`
- **Excel**: Cột C, D, E tự động cập nhật tên file hoặc trạng thái lỗi

## Cấu hình

Mở file `find.py` và chỉnh sửa:

```python
# Thư mục lưu ảnh
FOLDER_NAME = "hinh_anh_san_pham"

# File Excel
EXCEL_FILE = "DSSP.xlsx"

# Số browser chạy song song (3 khuyến nghị)
NUM_WORKERS = 3

# Chạy ẩn (không hiện trình duyệt)
# chrome_options.add_argument("--headless")  # Bỏ comment để bật
```

**Khuyến nghị về NUM_WORKERS:**
- **3 workers** (khuyến nghị): Ổn định nhất, phù hợp mọi máy 8GB+ RAM
- **4-5 workers**: Chỉ dùng nếu máy có 16GB+ RAM và muốn tăng tốc
- ⚠️ **Lưu ý**: Quá nhiều workers có thể gây:
  - Chrome crash do thiếu RAM
  - Google phát hiện và chặn
  - File Excel bị corrupt (đã fix bằng thread-safe lock)

## Xử lý lỗi

### Lỗi: "Bad CRC-32 for file 'xl/worksheets/sheet1.xml'"

**Nguyên nhân**: File Excel bị corrupt do đang mở hoặc bị ghi đồng thời

**Giải pháp**:
1. ⚠️ **Đóng file Excel** trước khi chạy script
2. Nếu file đã bị corrupt:
   - Backup file DSSP.xlsx
   - Mở bằng Excel và "Save As" với tên mới
   - Hoặc tạo lại file từ backup

### Lỗi: "Chrome instance exited" / "failed to write prefs file"

**Nguyên nhân**: Quá nhiều Chrome instances hoặc thiếu RAM

**Giải pháp**:
1. Giảm `NUM_WORKERS` xuống 2 hoặc 3
2. Đóng các ứng dụng khác để giải phóng RAM
3. Xóa thư mục `selenium_profile_worker_*` và chạy lại

### Lỗi: "Không tìm thấy ảnh"

- Google có thể thay đổi cấu trúc HTML
- Thử chạy lại sau vài phút
- Kiểm tra screenshot debug: `debug_*.png`

### Lỗi: CAPTCHA

- Google phát hiện quá nhiều request
- Giảm `NUM_WORKERS` xuống 2
- Tăng delay trong code (dòng `random.uniform(2, 3)` → `random.uniform(3, 5)`)
- Chạy lại sau 10-15 phút

## Lưu ý

⚠️ **Quan trọng:**

- ⚠️ **Đóng file Excel trước khi chạy** để tránh lỗi "Bad CRC-32"
- Không đóng cửa sổ Chrome khi script đang chạy
- Google có thể chặn nếu request quá nhanh
- Delay mặc định: 2-3 giây giữa mỗi request (đã tối ưu)
- Script tự động tạo profile riêng cho mỗi worker

💡 **Tips:**

- Chạy vào giờ thấp điểm để tránh bị chặn
- Nếu có nhiều sản phẩm (>100), chia nhỏ file Excel
- Kiểm tra kết quả trong Excel sau khi chạy xong
- Nếu bị lỗi giữa chừng, chạy lại script (sẽ skip sản phẩm đã có ảnh)
- Xóa thư mục `selenium_profile_worker_*` định kỳ để giải phóng dung lượng

## Troubleshooting

### Chrome không mở

```bash
# Cài lại webdriver-manager
pip install --upgrade webdriver-manager
```

### Không đọc được Excel

```bash
# Cài lại openpyxl
pip install --upgrade openpyxl
```

### Excel bị corrupt (Bad CRC-32)

```bash
# Xóa các profile cũ
rmdir /s /q selenium_profile_worker_0
rmdir /s /q selenium_profile_worker_1
rmdir /s /q selenium_profile_worker_2

# Hoặc trên Linux/Mac:
rm -rf selenium_profile_worker_*
```

### Ảnh tải về bị lỗi

- Kiểm tra kết nối internet
- Một số ảnh có thể bị bảo vệ bản quyền
- Thử tìm kiếm thủ công để xác nhận

### Script chạy chậm hoặc bị treo

- Giảm `NUM_WORKERS` xuống 2
- Kiểm tra RAM còn trống (Task Manager)
- Đóng các ứng dụng khác

## License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## Tác giả

Phát triển bởi AI Assistant với sự hỗ trợ của Kiro IDE.

## Changelog

### v2.4.0 (2024-11-27)

- ✅ **Tự động chọn ảnh kế tiếp**: Khi không tải được ảnh, tự động thử ảnh tiếp theo
- ✅ **Luôn cố gắng lấy đủ 3 ảnh**: Lặp qua tối đa 15 ảnh để tìm 3 ảnh tốt
- ✅ **Logging chi tiết**: Hiển thị "✓ Đã tải ảnh 1/3", "✗ Không tải được, thử ảnh tiếp theo"
- ✅ Giảm thiểu lỗi "LỖI_ẢNH" trong Excel

### v2.3.0 (2024-11-27)

- ✅ **Tìm kiếm thông minh**: Kết hợp barcode + tên sản phẩm để tăng độ chính xác
- ✅ Giảm thiểu ảnh sai do tìm kiếm chỉ bằng barcode

### v2.2.0 (2024-11-27)

- ✅ **Chuyển từ Multiprocessing sang Threading**: Fix lỗi "Bad CRC-32" trên Windows
- ✅ **Thread-safe Excel writing**: Sử dụng `threading.Lock` thay vì `multiprocessing.Lock`
- ✅ **Profile riêng cho mỗi thread**: Tránh xung đột "failed to write prefs file"
- ✅ **Progress tracking**: Hiển thị "X/Y sản phẩm hoàn thành"
- ✅ Giảm startup delay xuống 0.3-1.0s (threads nhẹ hơn processes)

### v2.1.0 (2024-11-27)

- ✅ **Multiprocessing**: Chạy 3 browser song song (tăng tốc 3x)
- ✅ Giảm delay xuống 2-3s (từ 3-5s)
- ✅ Thread-safe Excel writing với Lock
- ✅ Mỗi worker có profile riêng

### v2.0.0 (2024-11-27)

- ✅ **Tải 3 ảnh đầu tiên** cho mỗi sản phẩm
- ✅ Đánh số thứ tự ảnh (_1, _2, _3)
- ✅ Ghi 3 đường dẫn vào 3 cột Excel riêng biệt

### v1.0.0 (2024-11-27)

- ✅ Tìm kiếm và tải ảnh từ Google Images
- ✅ Đọc/ghi Excel tự động
- ✅ Tên file không dấu với underscore
- ✅ Anti-detection và Chrome profile
- ✅ Xử lý lỗi và screenshot debug
