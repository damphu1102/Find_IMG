# Hệ thống Tự động Tải Hình Ảnh Sản Phẩm

Công cụ tự động tìm kiếm và tải hình ảnh sản phẩm từ Google Images dựa trên danh sách trong file Excel.

## Tính năng

- ✅ Đọc danh sách sản phẩm từ file Excel (DSSP.xlsx)
- ✅ Tự động tìm kiếm trên Google Images
- ✅ Click vào ảnh để lấy phiên bản full size (chất lượng cao)
- ✅ Tải ảnh về thư mục `hinh_anh_san_pham`
- ✅ Tự động ghi tên file ảnh vào Excel
- ✅ Tên file không dấu, thay khoảng trắng bằng `_`
- ✅ Sử dụng Chrome profile để tránh bị chặn
- ✅ Anti-detection (tránh bị phát hiện là bot)

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

Mở file `DSSP.xlsx` và nhập danh sách sản phẩm vào **cột A** (từ dòng 2 trở đi):

| Tên sản phẩm             | Tên file ảnh     |
| ------------------------ | ---------------- |
| iPhone 15 Pro Max 256GB  | _(tự động điền)_ |
| Samsung Galaxy S24 Ultra | _(tự động điền)_ |
| Chuột Logitech G102      | _(tự động điền)_ |

### 2. Chạy script

```bash
python find.py
```

### 3. Theo dõi quá trình

Script sẽ:

1. Mở Chrome với profile riêng
2. Truy cập Google Images
3. Tìm kiếm từng sản phẩm
4. Click vào ảnh đầu tiên để lấy full size
5. Tải ảnh về thư mục `hinh_anh_san_pham`
6. Ghi tên file vào cột B của Excel

### 4. Kết quả

- **Ảnh đã tải**: Lưu trong thư mục `hinh_anh_san_pham/`
- **Tên file**: Không dấu, dấu cách thay bằng `_`
  - Ví dụ: `iPhone_15_Pro_Max_256GB.jpg`
- **Excel**: Cột B tự động cập nhật tên file hoặc trạng thái lỗi

## Cấu hình

Mở file `find.py` và chỉnh sửa:

```python
# Thư mục lưu ảnh
FOLDER_NAME = "hinh_anh_san_pham"

# File Excel
EXCEL_FILE = "DSSP.xlsx"

# Chạy ẩn (không hiện trình duyệt)
# chrome_options.add_argument("--headless")  # Bỏ comment để bật
```

## Xử lý lỗi

### Lỗi: "Không tìm thấy ảnh"

- Google có thể thay đổi cấu trúc HTML
- Thử chạy lại sau vài phút
- Kiểm tra screenshot debug: `debug_*.png`

### Lỗi: "SessionNotCreatedException"

- Đóng tất cả cửa sổ Chrome trước khi chạy
- Hoặc script sẽ tự động dùng profile riêng

### Lỗi: CAPTCHA

- Google phát hiện quá nhiều request
- Tăng delay giữa các lần tìm kiếm
- Chạy lại sau 10-15 phút

### Excel bị lỗi khi ghi

- Đóng file Excel trước khi chạy script
- Kiểm tra quyền ghi file

## Lưu ý

⚠️ **Quan trọng:**

- Đóng tất cả Chrome trước khi chạy (hoặc script dùng profile riêng)
- Không đóng cửa sổ Chrome khi script đang chạy
- Google có thể chặn nếu request quá nhanh
- Delay mặc định: 3-5 giây giữa mỗi sản phẩm

💡 **Tips:**

- Chạy vào giờ thấp điểm để tránh bị chặn
- Nếu có nhiều sản phẩm, chia nhỏ file Excel
- Kiểm tra kết quả trong Excel sau khi chạy xong

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

### Ảnh tải về bị lỗi

- Kiểm tra kết nối internet
- Một số ảnh có thể bị bảo vệ bản quyền
- Thử tìm kiếm thủ công để xác nhận

## License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## Tác giả

Phát triển bởi AI Assistant với sự hỗ trợ của Kiro IDE.

## Changelog

### v1.0.0 (2024-11-27)

- ✅ Tìm kiếm và tải ảnh từ Google Images
- ✅ Đọc/ghi Excel tự động
- ✅ Tên file không dấu với underscore
- ✅ Anti-detection và Chrome profile
- ✅ Xử lý lỗi và screenshot debug
