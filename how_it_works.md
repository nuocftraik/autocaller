# 🚀 Hướng Dẫn Sử Dụng Autocaller v2.0

Chào mừng bạn đến với **Autocaller v2.0**! Đây là phiên bản nâng cấp toàn diện từ script đơn luồng `multi.py` cũ sang một hệ thống module chuyên nghiệp, hỗ trợ đa luồng, xoay vòng proxy, giao diện menu tương tác cực đẹp và thống kê báo cáo chi tiết.

---

## 📌 Các Tính Năng Nổi Bật

1. **Giao diện kép (Dual UI Mode):**
   * **TUI (Interactive Menu):** Giao diện đồ họa giả lập trên Terminal cực đẹp dùng thư viện `rich`, hỗ trợ chọn số điện thoại, số vòng lặp và tùy chỉnh bộ lọc.
   * **CLI (Command Line):** Chạy nhanh bằng dòng lệnh phù hợp cho các tác vụ tự động hóa (automation) hoặc tích hợp với tool khác.
2. **Auto-Discovery (Tự động nhận diện dịch vụ):**
   * Quản lý **80 dịch vụ OTP** gói gọn trong duy nhất một file `services/all_services.py`.
   * Hệ thống tự động quét và nạp các dịch vụ này vào chương trình tại thời điểm chạy mà không cần sửa code cốt lõi.
3. **Đa luồng hiệu năng cao (Multi-threading):**
   * Sử dụng `ThreadPoolExecutor` để chạy song song các yêu cầu gửi OTP, giúp tối ưu hóa tốc độ và băng thông.
4. **Xoay vòng Proxy (Proxy Rotation):**
   * Tự động xoay vòng danh sách IP từ file `proxies.txt` theo cơ chế ngẫu nhiên hoặc tuần tự cho từng request, giúp tránh bị chặn IP (IP block).
5. **Kiểm tra sức khỏe song song (Parallel Health Check):**
   * Kiểm tra trạng thái hoạt động của toàn bộ 80 dịch vụ cùng một lúc bằng đa luồng, hiển thị bảng đánh giá chi tiết chỉ trong vài giây.
6. **Mô phỏng chạy thử (Dry-run):**
   * Kiểm tra thứ tự và danh sách dịch vụ sẽ thực thi mà không gửi request thực tế lên máy chủ (không tốn tài nguyên và không gửi OTP thật).
7. **Tránh bị phát hiện (Anti-Spam & Randomize):**
   * Hỗ trợ trộn ngẫu nhiên thứ tự gọi dịch vụ (`randomize_order`) ở mỗi vòng lặp để tránh bị phát hiện pattern hành vi.
8. **Thống kê & Xuất báo cáo (Stats & Export):**
   * Thống kê trực quan thời gian phản hồi, tỷ lệ thành công/thất bại và hỗ trợ xuất báo cáo định dạng `JSON` hoặc `CSV`.
9. **Nhật ký thông minh (Logging):**
   * Ghi log song song ra màn hình và file lưu trữ trong thư mục `logs/` tự động phân tách theo ngày.

---

## 📂 Cấu Trúc Dự Án

```text
autocaller/
├── main.py              # File khởi chạy chính (Tự động nhận diện CLI/TUI)
├── config.yaml          # File cấu hình trung tâm (delay, thread, proxy, log...)
├── proxies.txt          # Danh sách proxy dùng để xoay vòng IP
├── requirements.txt     # Danh sách thư viện Python cần cài đặt
├── multi.py             # File script cũ (dùng làm bản sao lưu)
├── how_it_works.md      # Tài liệu hướng dẫn sử dụng (chính là file này)
├── core/                # Thư mục lõi hệ thống
│   ├── base_service.py  # Định nghĩa class cha Service và cấu trúc kết quả
│   ├── config.py        # Module đọc và kiểm tra tính hợp lệ của config.yaml
│   ├── http_client.py   # Quản lý HTTP Session, tự động cấu hình Retry và Proxy
│   ├── logger.py        # Thiết lập ghi nhật ký ra console (có màu) và file
│   ├── proxy_manager.py # Quản lý xoay vòng proxy
│   ├── runner.py        # Bộ điều phối đa luồng chính (chạy OTP & Health Check)
│   └── stats.py         # Quản lý số liệu thống kê và xuất báo cáo
├── services/            # Thư mục chứa định nghĩa API của dịch vụ
│   ├── __init__.py      # Module quét và nạp động (auto-discover) các service
│   ├── _template.py     # Template mẫu để viết thêm service mới sau này
│   └── all_services.py  # File chứa code thực thi của toàn bộ 80 dịch vụ OTP
├── ui/                  # Thư mục giao diện người dùng
│   ├── cli.py           # Logic xử lý giao diện dòng lệnh (CLI)
│   └── tui.py           # Logic xử lý giao diện menu tương tác (TUI)
└── logs/                # Thư mục chứa file log tự động tạo khi chạy
```

---

## 🛠️ Hướng Dẫn Cài Đặt

Mở Terminal (CMD / PowerShell / Bash) tại thư mục `autocaller` và chạy các lệnh sau:

### Bước 1: Cài đặt thư viện phụ thuộc
```powershell
pip install -r requirements.txt
```
*(Hoặc tự cài thủ công: `pip install requests pyyaml rich urllib3`)*

### Bước 2: Chuẩn bị Proxy (Tùy chọn)
Nếu muốn dùng tính năng đổi IP, hãy copy danh sách proxy của bạn dán vào file `proxies.txt` theo định dạng:
```text
http://ip_proxy:port
http://user:password@ip_proxy:port
```
Sau đó mở file `config.yaml`, chỉnh sửa ở phần `proxy` thành:
```yaml
proxy:
  enabled: true
```

---

## 🚀 Hướng Dẫn Chạy Chương Trình

### 1. Chạy Giao Diện Menu Tương Tác (TUI)
Chỉ cần chạy lệnh sau mà không truyền thêm tham số:
```powershell
python main.py
```
Giao diện menu dạng bảng sẽ hiện ra. Bạn có thể:
*   Nhập số `1` để bắt đầu gửi OTP.
*   Nhập số `2` để xem danh sách 80 dịch vụ hiện có.
*   Nhập số `3` để chạy kiểm tra sức khỏe của API.
*   Nhập số `4` để xem nhanh cấu hình hiện tại.

---

### 2. Chạy Bằng Dòng Lệnh (CLI)
Chế độ này rất hữu ích khi bạn muốn tích hợp công cụ vào một script tự động khác.

*   **Chạy gửi OTP cơ bản cho 1 hoặc nhiều số điện thoại:**
    ```powershell
    python main.py --phone 0357156329 --count 3
    ```
    *(Gửi OTP đến số `0357156329`, lặp lại 3 vòng)*

    ```powershell
    python main.py --phone 0357156329 0901234567 --count 1
    ```
    *(Gửi OTP song song cho cả 2 số điện thoại)*

*   **Lọc chạy theo nhóm dịch vụ cụ thể (Category):**
    Các nhóm hỗ trợ: `telecom`, `ecommerce`, `fnb`, `delivery`, `finance`, `education`, `realestate`, `other`.
    ```powershell
    python main.py --phone 0357156329 --count 2 --category telecom fnb
    ```
    *(Chỉ chạy các dịch vụ thuộc nhóm Viễn thông và Ăn uống)*

*   **Chỉ chạy một vài dịch vụ cụ thể theo tên:**
    ```powershell
    python main.py --phone 0357156329 --count 1 --service TV360 VieON MyTV
    ```

*   **Xem danh sách tất cả dịch vụ đang có kèm mô tả:**
    ```powershell
    python main.py --list-services
    ```

*   **Kiểm tra sức khỏe song song toàn bộ API:**
    ```powershell
    python main.py --health-check --phone 0357156329
    ```
    *(Hệ thống sẽ ping thử đồng thời đến toàn bộ 80 dịch vụ và báo dịch vụ nào còn hoạt động hoặc đã chết)*

*   **Chạy mô phỏng (Dry-run):**
    ```powershell
    python main.py --phone 0357156329 --count 1 --dry-run
    ```
    *(Chỉ hiển thị danh sách và thứ tự dịch vụ sẽ gọi, không gửi yêu cầu thật)*

*   **Chạy và tự động xuất báo cáo kết quả:**
    ```powershell
    python main.py --phone 0357156329 --count 1 --export json
    # Hoặc xuất dạng CSV
    python main.py --phone 0357156329 --count 1 --export csv
    ```
    *(Báo cáo kết quả chi tiết từng dịch vụ sẽ được tạo ở thư mục gốc)*

---

## ⚙️ Hướng Dẫn Cấu Hình (`config.yaml`)

Mở file `config.yaml` để tinh chỉnh các thông số hoạt động của hệ thống:

```yaml
general:
  max_count: 200              # Số vòng lặp tối đa cho phép chạy
  delay_between_services: 1.0 # Thời gian nghỉ giữa việc kích hoạt các thread dịch vụ (giây)
  delay_between_rounds: 5.0   # Thời gian nghỉ sau khi hoàn thành 1 vòng lặp để chuẩn bị vòng kế tiếp (giây)
  randomize_order: true       # Tráo đổi ngẫu nhiên thứ tự các dịch vụ ở mỗi vòng để chống spam pattern

threading:
  max_workers: 10             # Số luồng (thread) chạy song song tối đa cùng lúc. Tăng lên để chạy nhanh hơn.

http:
  timeout: 15                 # Thời gian tối đa chờ phản hồi từ API (giây). 
  verify_ssl: false           # Bỏ qua xác thực SSL (giúp chạy mượt hơn với một số API chứng chỉ lỗi)
  retry_count: 2              # Số lần thử lại nếu yêu cầu HTTP thất bại
  retry_backoff: 1.5          # Thời gian giãn cách giữa các lần thử lại (nhân hệ số 1.5)

proxy:
  enabled: false              # Chuyển thành true để bật xoay vòng proxy
  file: "proxies.txt"         # Đường dẫn file danh sách proxy
  rotate: true                # Tự động xoay vòng proxy sau mỗi request

logging:
  level: "INFO"               # Cấp độ log hiển thị (DEBUG | INFO | WARNING | ERROR)
  file_enabled: true          # Bật ghi log ra file
  file_dir: "logs"            # Thư mục lưu trữ log
```

---

## ➕ Cách Thêm Dịch Vụ Mới

Nếu bạn tìm thấy một API gửi OTP mới và muốn thêm vào dự án, bạn không cần phải sửa cấu trúc hệ thống. Hãy làm theo các bước sau:

1. Mở file [services/all_services.py](file:///d:/MyCode/autocaller/services/all_services.py).
2. Cuộn xuống cuối file và viết thêm một class kế thừa từ class cha `Service`. Ví dụ:
   ```python
   class ShopeeOTP(Service):
       name = "Shopee"                      # Tên hiển thị trên bảng
       category = "ecommerce"               # Nhóm dịch vụ
       active = True                        # Trạng thái kích hoạt
       description = "Shopee - OTP đăng nhập" # Mô tả ngắn

       def execute(self, phone: str, phone_intl: str) -> ServiceResult:
           # Gửi yêu cầu sử dụng self.session đã có sẵn Proxy & Retry
           response = self.session.post(
               url="https://api.shopee.vn/api/v2/login/send_otp",
               headers={
                   "Content-Type": "application/json",
                   "User-Agent": "Mozilla/5.0 ...",
               },
               json={
                   "phone": phone  # Sử dụng biến phone nhận vào
               },
               timeout=self.config["http"]["timeout"] # Sử dụng timeout từ file cấu hình
           )
           # Trả về kết quả chuẩn hóa
           return ServiceResult(
               success=response.ok,
               message=response.text[:200],
               status_code=response.status_code
           )
   ```
3. Lưu file lại. Lần chạy tiếp theo hệ thống sẽ tự động quét thấy dịch vụ `Shopee` và nạp vào danh sách!