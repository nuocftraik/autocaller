"""
base_service.py — Base class cho tất cả OTP service.

Mỗi service kế thừa class Service và chỉ cần override:
  - name, category, description
  - execute(phone, phone_intl) → ServiceResult
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import time


@dataclass
class ServiceResult:
    """Kết quả trả về sau khi gọi 1 service."""
    success: bool
    service_name: str = ""
    message: str = ""
    status_code: int = 0
    response_time_ms: float = 0.0
    phone: str = ""
    error: Optional[str] = None


class Service(ABC):
    """
    Base class cho tất cả OTP service.
    
    Cách dùng:
        class MyService(Service):
            name = "MyService"
            category = "ecommerce"
            
            def execute(self, phone, phone_intl):
                resp = self.session.post(url, json={"phone": phone})
                return ServiceResult(success=resp.ok, ...)
    """

    # --- Metadata (override trong subclass) ---
    name: str = "Unknown"
    category: str = "other"         # telecom | ecommerce | fnb | delivery | finance | education | realestate | other
    active: bool = True             # False = bỏ qua khi chạy
    description: str = ""

    def __init__(self, session, config: dict):
        """
        Args:
            session: requests.Session đã cấu hình sẵn (retry, proxy, SSL).
            config: dict config từ config.yaml.
        """
        self.session = session
        self.config = config

    @abstractmethod
    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        """
        Gửi request OTP đến service.

        Args:
            phone: Số điện thoại gốc (e.g. "0357156329")
            phone_intl: Số quốc tế (e.g. "+84357156329")

        Returns:
            ServiceResult với success=True/False và thông tin kèm theo.
        """
        pass

    def safe_execute(self, phone: str, phone_intl: str) -> ServiceResult:
        """
        Wrapper an toàn cho execute() — bắt mọi exception,
        đo thời gian response, và trả về ServiceResult.
        Nâng cao: Tự động phân tích response body để loại bỏ các trường hợp
        phản hồi HTTP 200 OK nhưng thực chất là thông báo lỗi nghiệp vụ.
        """
        start = time.perf_counter()
        try:
            result = self.execute(phone, phone_intl)
            result.service_name = self.name
            result.phone = phone_intl
            result.response_time_ms = (time.perf_counter() - start) * 1000
            
            # Phân tích nội dung response để phát hiện lỗi nghiệp vụ ẩn dưới HTTP 200
            if result.success and result.message:
                msg_lower = result.message.lower()
                
                # 1. Phát hiện chặn bảo mật (Cloudflare, IP block)
                if any(x in msg_lower for x in ["cloudflare", "access denied", "blocked", "security check", "bảo mật", "forbidden"]):
                    result.success = False
                    result.error = "Bị chặn (Cloudflare/IP Block/WAF)"
                
                # 2. Phát hiện yêu cầu Captcha
                elif any(x in msg_lower for x in ["captcha", "invalid_captcha"]):
                    result.success = False
                    result.error = "Yêu cầu Captcha (Không thể tự động gửi)"
                
                # 3. Phát hiện lỗi 404 lồng trong response
                elif '"code":404' in msg_lower or '"code": 404' in msg_lower or '"status":404' in msg_lower:
                    result.success = False
                    result.error = "Lỗi API 404 (Endpoint thay đổi)"
                
                # 4. Phân tích cú pháp JSON để tìm các cờ báo lỗi
                else:
                    try:
                        import json
                        data = json.loads(result.message)
                        if isinstance(data, dict):
                            # Kiểm tra trường success hoặc status trực tiếp
                            success_val = data.get("success")
                            status_val = data.get("status")
                            
                            # Nếu success trả về False rõ ràng
                            if success_val is False:
                                err_msg = data.get("message") or data.get("error") or "success=False"
                                result.success = False
                                result.error = f"API Thất bại: {err_msg}"
                            
                            # Nếu status trả về các chuỗi lỗi phổ biến
                            elif status_val in ["fail", "failed", "error", "err"]:
                                err_msg = data.get("message") or data.get("error") or f"status={status_val}"
                                result.success = False
                                result.error = f"API Thất bại: {err_msg}"
                            
                            else:
                                # Kiểm tra các trường mã lỗi (error code) hoặc thông báo lỗi lồng
                                error_code = data.get("error_code") or data.get("errorCode") or data.get("code")
                                error_msg = data.get("error_msg") or data.get("error_message") or data.get("message")
                                
                                # Lỗi dạng lồng như {"error": {"code": 1201, "message": "..."}}
                                error_obj = data.get("error")
                                errors_list = data.get("errors")
                                
                                # Xử lý lỗi dạng list errors
                                if errors_list and isinstance(errors_list, list) and len(errors_list) > 0:
                                    first_err = errors_list[0]
                                    if isinstance(first_err, dict):
                                        err_code = first_err.get("code")
                                        err_msg = first_err.get("message") or first_err.get("error")
                                        if "limit" not in str(err_msg).lower() and "giới hạn" not in str(err_msg).lower():
                                            result.success = False
                                            result.error = f"Lỗi API ({err_code}): {err_msg}"
                                
                                # Xử lý lỗi dạng object error
                                elif error_obj and isinstance(error_obj, dict):
                                    err_code = error_obj.get("code")
                                    err_msg = error_obj.get("message") or error_obj.get("error")
                                    if err_code not in [None, 0, "0", "success", "SUCCESS"]:
                                        if "limit" not in str(err_msg).lower() and "giới hạn" not in str(err_msg).lower():
                                            result.success = False
                                            result.error = f"Lỗi API ({err_code}): {err_msg}"
                                
                                # Xử lý mã lỗi ở root level
                                elif error_code not in [None, 0, "0", "success", "SUCCESS", 200, "200"]:
                                    # Ngoại lệ cho rate limits (vẫn tính là Active vì API sống)
                                    if any(x in str(error_msg).lower() for x in ["limit", "giới hạn", "rate", "tần suất"]):
                                        pass
                                    else:
                                        result.success = False
                                        result.error = f"Lỗi API ({error_code}): {error_msg}"
                    except Exception:
                        pass
            
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return ServiceResult(
                success=False,
                service_name=self.name,
                phone=phone_intl,
                error=str(e),
                response_time_ms=elapsed,
            )

    def __repr__(self):
        status = "✅" if self.active else "❌"
        return f"{status} {self.name} [{self.category}]"
