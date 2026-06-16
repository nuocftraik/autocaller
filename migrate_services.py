"""
Script tạo tất cả service files từ multi.py.
Chạy 1 lần để migrate, sau đó xóa script này.
"""

import os
import sys
import random
import string

SERVICES_DIR = os.path.join(os.path.dirname(__file__), "services")

def generate_random_email(domain='example.com'):
    length = random.randint(5, 10)
    email_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f'{email_name}@{domain}'

# Mỗi tuple: (filename, class_name, name, category, description, phone_field, execute_body)
# phone_field: "phone" = dùng phone gốc, "phone_intl" = dùng +84xxx

SERVICES = [
    # ===== STREAMING =====
    {
        "file": "tv360.py",
        "class": "TV360",
        "name": "TV360",
        "category": "streaming",
        "desc": "Viettel TV360 - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "vieon.py",
        "class": "VieON",
        "name": "VieON",
        "category": "streaming",
        "desc": "VieON - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "mytv.py",
        "class": "MyTV",
        "name": "MyTV",
        "category": "streaming",
        "desc": "VNPT MyTV - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },

    # ===== TELECOM =====
    {
        "file": "myviettel.py",
        "class": "MyViettel",
        "name": "MyViettel",
        "category": "telecom",
        "desc": "MyViettel - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "vttelecom.py",
        "class": "VTTelecom",
        "name": "VTTelecom",
        "category": "telecom",
        "desc": "Viettel Telecom - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "mocha.py",
        "class": "Mocha",
        "name": "Mocha",
        "category": "telecom",
        "desc": "Mocha Video - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "mocha2.py",
        "class": "Mocha2",
        "name": "Mocha2",
        "category": "telecom",
        "desc": "Mocha app - OTP v33",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "mocha35.py",
        "class": "Mocha35",
        "name": "Mocha35",
        "category": "telecom",
        "desc": "Mocha35 - OTP v32",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },

    # ===== ECOMMERCE =====
    {
        "file": "fptshop.py",
        "class": "FPTShop",
        "name": "FPTShop",
        "category": "ecommerce",
        "desc": "FPT Shop - OTP xác thực",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "hasaki.py",
        "class": "Hasaki",
        "name": "Hasaki",
        "category": "ecommerce",
        "desc": "Hasaki.vn - OTP xác thực (mobile API)",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "fahasa.py",
        "class": "Fahasa",
        "name": "Fahasa",
        "category": "ecommerce",
        "desc": "Fahasa - kiểm tra số điện thoại",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "bibomart.py",
        "class": "BiboMart",
        "name": "BiboMart",
        "category": "ecommerce",
        "desc": "BiboMart - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "liena.py",
        "class": "Liena",
        "name": "Liena",
        "category": "ecommerce",
        "desc": "Liena.com.vn - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "aio.py",
        "class": "AIO",
        "name": "AIO",
        "category": "ecommerce",
        "desc": "AIO Smart - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },

    # ===== FNB =====
    {
        "file": "befood.py",
        "class": "BeFood",
        "name": "BeFood",
        "category": "fnb",
        "desc": "Be Food - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "thecoffeehouse.py",
        "class": "TheCoffeeHouse",
        "name": "TheCoffeeHouse",
        "category": "fnb",
        "desc": "The Coffee House - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "highlands.py",
        "class": "Highlands",
        "name": "Highlands",
        "category": "fnb",
        "desc": "Highlands Coffee - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "goldenspoons_zl.py",
        "class": "GoldenSpoonsZL",
        "name": "GoldenSpoonsZL",
        "category": "fnb",
        "desc": "Golden Spoons - OTP via Zalo",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "goldenspoons_sms.py",
        "class": "GoldenSpoonsSMS",
        "name": "GoldenSpoonsSMS",
        "category": "fnb",
        "desc": "Golden Spoons - OTP via SMS",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "ilokafood.py",
        "class": "IlokaFood",
        "name": "IlokaFood",
        "category": "fnb",
        "desc": "Iloka Food - OTP Zalo",
        "code": '''
    def execute(self, phone, phone_intl):
        response = self.session.post(
            'http://back.iloka.vn:9999/api/v2/customer/sentZaloOTP',
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
            json={'phone': phone},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)
'''
    },

    # ===== DELIVERY =====
    {
        "file": "viettelpost.py",
        "class": "ViettelPost",
        "name": "ViettelPost",
        "category": "delivery",
        "desc": "ViettelPost - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "ahamove.py",
        "class": "AhaMove",
        "name": "AhaMove",
        "category": "delivery",
        "desc": "AhaMove - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
        # Step 1: Register
        import random, string
        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '@example.com'
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
'''
    },
    {
        "file": "jupviec.py",
        "class": "JupViec",
        "name": "JupViec",
        "category": "delivery",
        "desc": "JupViec - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "ghephang.py",
        "class": "GhePhang",
        "name": "GhePhang",
        "category": "delivery",
        "desc": "GhePhang - OTP SMS",
        "code": '''
    def execute(self, phone, phone_intl):
        response = self.session.get(
            'https://quanly.ghephang.com/gh/api_driver/send_otp_v2.json',
            params={'phone': phone, 'id_device': 'CFAA3646-4D74-43A4-ADAC-4240BBAF87BF', 'zalo': '0'},
            headers={'Accept': 'application/json, text/plain, */*', 'User-Agent': 'GhepHangKhachHang/22 CFNetwork/1494.0.7 Darwin/23.4.0'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)
'''
    },
    {
        "file": "ghephang_zl.py",
        "class": "GhePhangZL",
        "name": "GhePhangZL",
        "category": "delivery",
        "desc": "GhePhang - OTP Zalo",
        "code": '''
    def execute(self, phone, phone_intl):
        response = self.session.get(
            'https://quanly.ghephang.com/gh/api_driver/send_otp_v2.json',
            params={'phone': phone, 'id_device': 'CFAA3646-4D74-43A4-ADAC-4240BBAF87BF', 'zalo': '1'},
            headers={'Accept': 'application/json, text/plain, */*', 'User-Agent': 'GhepHangKhachHang/22 CFNetwork/1494.0.7 Darwin/23.4.0'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)
'''
    },

    # ===== FINANCE =====
    {
        "file": "vnsc.py",
        "class": "VNSC",
        "name": "VNSC",
        "category": "finance",
        "desc": "Vina Securities - OTP xác thực",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "vietmoney.py",
        "class": "VietMoney",
        "name": "VietMoney",
        "category": "finance",
        "desc": "VietMoney - OTP đăng ký (SMS)",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "sfin.py",
        "class": "SFin",
        "name": "SFin",
        "category": "finance",
        "desc": "SFin/SShop - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },

    # ===== EDUCATION =====
    {
        "file": "vuihoc.py",
        "class": "VuiHoc",
        "name": "VuiHoc",
        "category": "education",
        "desc": "VuiHoc - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "prepedu.py",
        "class": "PrepEdu",
        "name": "PrepEdu",
        "category": "education",
        "desc": "PrepEdu - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "babilala.py",
        "class": "Babilala",
        "name": "Babilala",
        "category": "education",
        "desc": "Babilala - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },

    # ===== REALESTATE =====
    {
        "file": "meeyland.py",
        "class": "MeeyLand",
        "name": "MeeyLand",
        "category": "realestate",
        "desc": "MeeyLand - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "atmnha.py",
        "class": "ATMNha",
        "name": "ATMNha",
        "category": "realestate",
        "desc": "ATM Nhà - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
                'query': 'mutation sendCode($phone: String!, $type: SendVerificationCodeType, $identifier: String!) {\\n  sendCode(phone: $phone, type: $type, identifier: $identifier) {\\n    payload\\n    success\\n    msg\\n    __typename\\n  }\\n}',
            },
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)
'''
    },
    {
        "file": "lozido.py",
        "class": "Lozido",
        "name": "Lozido",
        "category": "realestate",
        "desc": "Lozido - OTP quản lý trọ",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },

    # ===== OTHER =====
    {
        "file": "vinwonders.py",
        "class": "VinWonders",
        "name": "VinWonders",
        "category": "other",
        "desc": "VinWonders/VinPearl - OTP booking",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "medigozl.py",
        "class": "MedigoZL",
        "name": "MedigoZL",
        "category": "other",
        "desc": "Medigo - OTP via Zalo",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "medigosms.py",
        "class": "MedigoSMS",
        "name": "MedigoSMS",
        "category": "other",
        "desc": "Medigo - OTP via SMS",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "dynaminds.py",
        "class": "Dynaminds",
        "name": "Dynaminds",
        "category": "other",
        "desc": "Dynaminds Hosting - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
        response = self.session.post(
            'https://api.dynaminds.vn/api/v1/oauth/register',
            headers={'Content-Type': 'application/json', 'User-Agent': 'Dynamic Hosting/1.4.1 CFNetwork/1494.0.7 Darwin/23.4.0'},
            json={'phone_number': phone, 'provider': 'self'},
            timeout=self.config["http"]["timeout"],
        )
        return ServiceResult(success=response.ok, message=response.text[:200], status_code=response.status_code)
'''
    },
    {
        "file": "vinfast_escooter.py",
        "class": "VinFastEScooter",
        "name": "VinFast eScooter",
        "category": "other",
        "desc": "VinFast eScooter - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "guvi.py",
        "class": "Guvi",
        "name": "Guvi",
        "category": "delivery",
        "desc": "Guvi - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "ting.py",
        "class": "Ting",
        "name": "Ting",
        "category": "other",
        "desc": "Ting.vn - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "kanow.py",
        "class": "Kanow",
        "name": "Kanow",
        "category": "other",
        "desc": "Kanow - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "unicar.py",
        "class": "UniCar",
        "name": "UniCar",
        "category": "other",
        "desc": "UniCar - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "vieclam24h.py",
        "class": "ViecLam24H",
        "name": "ViecLam24H",
        "category": "other",
        "desc": "ViecLam24H - OTP đăng nhập",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "upos.py",
        "class": "UPOS",
        "name": "UPOS",
        "category": "other",
        "desc": "UPOS - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
    {
        "file": "bigm.py",
        "class": "BigM",
        "name": "BigM",
        "category": "other",
        "desc": "BigM - OTP đăng ký",
        "code": '''
    def execute(self, phone, phone_intl):
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
'''
    },
]


def generate_service_file(svc):
    """Tạo nội dung file service."""
    return f'''"""Service: {svc["name"]} — {svc["desc"]}"""

from core.base_service import Service, ServiceResult


class {svc["class"]}(Service):
    name = "{svc["name"]}"
    category = "{svc["category"]}"
    active = True
    description = "{svc["desc"]}"
{svc["code"]}
'''


def main():
    os.makedirs(SERVICES_DIR, exist_ok=True)

    created = 0
    for svc in SERVICES:
        filepath = os.path.join(SERVICES_DIR, svc["file"])
        content = generate_service_file(svc)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"  ✅ {svc['file']} — {svc['name']}")

    print(f"\n🎉 Đã tạo {created} service files trong {SERVICES_DIR}")


if __name__ == "__main__":
    main()
