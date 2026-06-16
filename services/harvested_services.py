"""
services/harvested_services.py — Tự động sinh bởi Harvester.
"""

from core.base_service import Service, ServiceResult


class Vuihoc(Service):
    name = "Vuihoc"
    category = "other"
    active = True
    description = "Tự động quét bởi Harvester"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        url = "https://vuihoc.vn/service/security/verifySignup"
        headers = {
            'referer': "https://vuihoc.vn/",
            'x-requested-with': "XMLHttpRequest",
            'accept': "application/json, text/javascript, */*; q=0.01",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        }
        data = f"data%5B0%5D%5Bname%5D=name&data%5B0%5D%5Bvalue%5D=adumemay&data%5B1%5D%5Bname%5D=email&data%5B1%5D%5Bvalue%5D={phone}&data%5B2%5D%5Bname%5D=password&data%5B2%5D%5Bvalue%5D=a999aca7f3731dfde7cdd46a83b87f72&data%5B3%5D%5Bname%5D=repass&data%5B3%5D%5Bvalue%5D=a999aca7f3731dfde7cdd46a83b87f72&data%5B4%5D%5Bname%5D=agree&data%5B4%5D%5Bvalue%5D=on&data%5B5%5D%5Bname%5D=csrf_token&data%5B5%5D%5Bvalue%5D=csrf-sign-up-ICKj69hBRv&url=https%3A%2F%2Fvuihoc.vn%2F"
        response = self.session.post(
            url,
            headers=headers,
            data=data,
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)
