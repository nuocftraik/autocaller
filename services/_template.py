"""
_template.py — Template để tạo service mới.

Hướng dẫn:
  1. Copy file này: cp _template.py ten_service.py
  2. Đổi tên class, name, category, description
  3. Implement execute() — chỉ cần gửi request và return ServiceResult
  4. Done! Service sẽ tự động được discover.

Lưu ý:
  - KHÔNG cần try/except — base class đã xử lý qua safe_execute()
  - KHÔNG dùng biến global — phone truyền qua tham số
  - self.session đã có retry + proxy + connection pool
  - Dùng self.config["http"]["timeout"] cho timeout
"""

from core.base_service import Service, ServiceResult


class TemplateService(Service):
    name = "TÊN_SERVICE"
    category = "other"  # telecom | ecommerce | fnb | delivery | finance | education | realestate | other
    active = False  # Đổi thành True khi sẵn sàng
    description = "Mô tả ngắn về service này"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        """
        Args:
            phone: Số gốc (e.g. "0357156329")
            phone_intl: Số quốc tế (e.g. "+84357156329")
        """
        response = self.session.post(
            url="https://api.example.com/send-otp",
            headers={
                "content-type": "application/json",
                "user-agent": "Mozilla/5.0",
            },
            json={
                "phone": phone,
            },
            timeout=self.config["http"]["timeout"],
        )

        return ServiceResult(
            success=response.ok,
            message=response.text[:200],
            status_code=response.status_code,
        )
