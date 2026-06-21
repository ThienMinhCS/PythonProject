# test_all_api.py
"""
File test API tổng hợp cho hệ thống đặt vé máy bay
Chạy: python test_all_api.py
"""

import httpx
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Optional

BASE_URL = "http://localhost:8000"

class Colors:
    """Màu sắc cho console output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.results = []
    
    def add(self, name: str, passed: bool, message: str = ""):
        self.total += 1
        if passed:
            self.passed += 1
            status = f"{Colors.GREEN}✅ PASS{Colors.RESET}"
        else:
            self.failed += 1
            status = f"{Colors.RED}❌ FAIL{Colors.RESET}"
        
        self.results.append({
            "name": name,
            "passed": passed,
            "message": message
        })
        print(f"  {status} {name}")
        if message:
            print(f"      {message}")
    
    def summary(self):
        print("\n" + "=" * 60)
        print(f"{Colors.BOLD}📊 TEST SUMMARY{Colors.RESET}")
        print("=" * 60)
        print(f"  ✅ Passed: {Colors.GREEN}{self.passed}{Colors.RESET}")
        print(f"  ❌ Failed: {Colors.RED}{self.failed}{Colors.RESET}")
        print(f"  📝 Total:  {self.total}")
        print(f"  📈 Rate:   {(self.passed/self.total*100):.1f}%" if self.total > 0 else "N/A")
        print("=" * 60)
        
        if self.failed > 0:
            print(f"\n{Colors.RED}❌ Failed tests:{Colors.RESET}")
            for r in self.results:
                if not r["passed"]:
                    print(f"  - {r['name']}: {r['message']}")

class APITester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_result = TestResult()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.test_user_email = f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        self.booking_id: Optional[int] = None
        self.flight_id: Optional[int] = None
        self.promotion_id: Optional[int] = None
    
    async def close(self):
        await self.client.aclose()
    
    def print_header(self, title: str):
        print("\n" + "=" * 60)
        print(f"{Colors.BOLD}{Colors.CYAN}🧪 {title}{Colors.RESET}")
        print("=" * 60)
    
    # ==================== 1. AUTH TESTS ====================
    
    async def test_register(self) -> bool:
        """Test đăng ký tài khoản mới"""
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/register",
                json={
                    "full_name": "Test User",
                    "email": self.test_user_email,
                    "password": "Test@123456",
                    "phone": "0987654321"
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                return True, "Đăng ký thành công"
            return False, f"Status: {response.status_code} - {response.text}"
        except Exception as e:
            return False, str(e)
    
    async def test_register_duplicate(self) -> bool:
        """Test đăng ký với email đã tồn tại"""
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/register",
                json={
                    "full_name": "Duplicate User",
                    "email": self.test_user_email,
                    "password": "Test@123456",
                    "phone": "0912345678"
                }
            )
            return response.status_code == 400, "Lỗi trùng email (expected)"
        except Exception as e:
            return False, str(e)
    
    async def test_login(self) -> bool:
        """Test đăng nhập"""
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/login",
                data={
                    "username": self.test_user_email,
                    "password": "Test@123456"
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                return True, "Đăng nhập thành công"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    async def test_login_wrong_password(self) -> bool:
        """Test đăng nhập sai mật khẩu"""
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/login",
                data={
                    "username": self.test_user_email,
                    "password": "WrongPassword123"
                }
            )
            return response.status_code == 401, "Sai mật khẩu (expected)"
        except Exception as e:
            return False, str(e)
    
    # ==================== 2. USER TESTS ====================
    
    async def test_get_current_user(self) -> bool:
        """Test lấy thông tin user hiện tại"""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.get(
                f"{BASE_URL}/users/me",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                return True, f"User: {data.get('full_name')} - {data.get('email')}"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    async def test_update_user(self) -> bool:
        """Test cập nhật thông tin user"""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.put(
                f"{BASE_URL}/users/me",
                headers=headers,
                json={
                    "full_name": "Updated Test User",
                    "phone": "0909090909"
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("full_name") == "Updated Test User", "Cập nhật thành công"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    # ==================== 3. FLIGHT TESTS ====================
    
    async def test_search_flights(self) -> bool:
        """Test tìm kiếm chuyến bay"""
        try:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            response = await self.client.get(
                f"{BASE_URL}/flights/search",
                params={
                    "departure": "SGN",
                    "arrival": "HAN",
                    "date": tomorrow,
                    "passengers": 1,
                    "seat_class": "Economy"
                }
            )
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    self.flight_id = data[0].get("flight_id")
                    return True, f"Tìm thấy {len(data)} chuyến bay"
                return True, "Không có chuyến bay (có thể do data)"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    async def test_search_flights_return(self) -> bool:
        """Test tìm kiếm chuyến bay khứ hồi"""
        try:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            day_after = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            response = await self.client.get(
                f"{BASE_URL}/flights/search",
                params={
                    "departure": "SGN",
                    "arrival": "HAN",
                    "date": tomorrow,
                    "return_date": day_after,
                    "passengers": 1,
                    "seat_class": "Economy"
                }
            )
            return response.status_code == 200, "Tìm kiếm khứ hồi thành công"
        except Exception as e:
            return False, str(e)
    
    async def test_get_flight_detail(self) -> bool:
        """Test lấy chi tiết chuyến bay"""
        if not self.flight_id:
            return False, "Chưa có flight_id"
        try:
            response = await self.client.get(
                f"{BASE_URL}/flights/{self.flight_id}"
            )
            if response.status_code == 200:
                data = response.json()
                return True, f"Chi tiết chuyến bay: {data.get('flight_number')}"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    # ==================== 4. BOOKING TESTS ====================
    
    async def test_create_booking(self) -> bool:
        """Test tạo đặt vé mới"""
        if not self.flight_id:
            return False, "Chưa có flight_id"
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.post(
                f"{BASE_URL}/bookings/",
                headers=headers,
                json={
                    "flight_id": self.flight_id,
                    "seat_class": "Economy",
                    "passengers": [
                        {
                            "full_name": "Nguyen Van A",
                            "gender": "Male",
                            "date_of_birth": "1990-01-15",
                            "nationality": "Vietnam",
                            "identifier_type": "Passport",
                            "identifier_number": "B12345678"
                        },
                        {
                            "full_name": "Tran Thi B",
                            "gender": "Female",
                            "date_of_birth": "1992-05-20",
                            "nationality": "Vietnam",
                            "identifier_type": "ID Card",
                            "identifier_number": "012345678901"
                        }
                    ]
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.booking_id = data.get("booking_id")
                return True, f"Tạo booking thành công - ID: {self.booking_id}"
            return False, f"Status: {response.status_code} - {response.text}"
        except Exception as e:
            return False, str(e)
    
    async def test_get_my_bookings(self) -> bool:
        """Test lấy danh sách đặt vé của user"""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.get(
                f"{BASE_URL}/bookings/my-bookings",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                return True, f"Lấy được {len(data)} booking"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    async def test_get_booking_detail(self) -> bool:
        """Test lấy chi tiết đặt vé"""
        if not self.booking_id:
            return False, "Chưa có booking_id"
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.get(
                f"{BASE_URL}/bookings/{self.booking_id}",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                return True, f"Booking #{self.booking_id}: {data.get('status')}"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    # ==================== 5. PROMOTION TESTS ====================
    
    async def test_apply_promotion(self) -> bool:
        """Test áp dụng mã khuyến mãi"""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.post(
                f"{BASE_URL}/promotions/apply",
                headers=headers,
                json={
                    "promo_code": "SUMMER2024",
                    "order_amount": 1000000
                }
            )
            # Promotion có thể không tồn tại, nên check 200 hoặc 404
            if response.status_code in [200, 404, 400]:
                return True, f"Áp dụng promotion: {response.status_code}"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    # ==================== 6. PAYMENT TESTS ====================
    
    async def test_create_payment(self) -> bool:
        """Test tạo thanh toán"""
        if not self.booking_id:
            return False, "Chưa có booking_id"
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.post(
                f"{BASE_URL}/payments/",
                headers=headers,
                json={
                    "booking_id": self.booking_id,
                    "amount": 1000000,
                    "payment_method": "Credit Card"
                }
            )
            if response.status_code == 200:
                data = response.json()
                return True, f"Thanh toán thành công - ID: {data.get('payment_id')}"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    # ==================== 7. ADMIN TESTS ====================
    
    async def test_admin_login(self) -> bool:
        """Test đăng nhập admin"""
        try:
            response = await self.client.post(
                f"{BASE_URL}/auth/login",
                data={
                    "username": "admin@airline.com",
                    "password": "admin123"
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                return True, "Đăng nhập admin thành công"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    async def test_admin_dashboard(self) -> bool:
        """Test dashboard admin"""
        if not hasattr(self, 'admin_token'):
            return False, "Chưa đăng nhập admin"
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = await self.client.get(
                f"{BASE_URL}/admin/dashboard",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                return True, f"Dashboard: {data}"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    async def test_admin_get_users(self) -> bool:
        """Test lấy danh sách users (admin)"""
        if not hasattr(self, 'admin_token'):
            return False, "Chưa đăng nhập admin"
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = await self.client.get(
                f"{BASE_URL}/admin/users?page=1&limit=10",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                return True, f"Lấy được {len(data) if isinstance(data, list) else '?'} users"
            return False, f"Status: {response.status_code}"
        except Exception as e:
            return False, str(e)

    # ==================== RUN ALL TESTS ====================

    async def run_all_tests(self):
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("=" * 60)
        print("  🚀 AIRLINE BOOKING SYSTEM - API TEST")
        print("=" * 60)
        print(f"{Colors.RESET}")
        print(f"  📍 Base URL: {BASE_URL}")
        print(f"  👤 Test User: {self.test_user_email}")
        print(f"  🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # === AUTH TESTS ===
        self.print_header("1. AUTHENTICATION TESTS")
        
        passed, msg = await self.test_register()
        self.test_result.add("Đăng ký tài khoản", passed, msg)
        
        passed, msg = await self.test_register_duplicate()
        self.test_result.add("Đăng ký trùng email", passed, msg)
        
        passed, msg = await self.test_login()
        self.test_result.add("Đăng nhập", passed, msg)
        
        passed, msg = await self.test_login_wrong_password()
        self.test_result.add("Đăng nhập sai mật khẩu", passed, msg)
        
        # === USER TESTS ===
        self.print_header("2. USER TESTS")
        
        passed, msg = await self.test_get_current_user()
        self.test_result.add("Lấy thông tin user", passed, msg)
        
        passed, msg = await self.test_update_user()
        self.test_result.add("Cập nhật thông tin user", passed, msg)
        
        # === FLIGHT TESTS ===
        self.print_header("3. FLIGHT TESTS")
        
        passed, msg = await self.test_search_flights()
        self.test_result.add("Tìm kiếm chuyến bay", passed, msg)
        
        passed, msg = await self.test_search_flights_return()
        self.test_result.add("Tìm kiếm khứ hồi", passed, msg)
        
        passed, msg = await self.test_get_flight_detail()
        self.test_result.add("Chi tiết chuyến bay", passed, msg)
        
        # === BOOKING TESTS ===
        self.print_header("4. BOOKING TESTS")
        
        passed, msg = await self.test_create_booking()
        self.test_result.add("Tạo đặt vé", passed, msg)
        
        passed, msg = await self.test_get_my_bookings()
        self.test_result.add("Lấy danh sách booking", passed, msg)
        
        passed, msg = await self.test_get_booking_detail()
        self.test_result.add("Chi tiết booking", passed, msg)
        
        # === PROMOTION TESTS ===
        self.print_header("5. PROMOTION TESTS")
        
        passed, msg = await self.test_apply_promotion()
        self.test_result.add("Áp dụng khuyến mãi", passed, msg)
        
        # === PAYMENT TESTS ===
        self.print_header("6. PAYMENT TESTS")
        
        passed, msg = await self.test_create_payment()
        self.test_result.add("Tạo thanh toán", passed, msg)
        
        # === ADMIN TESTS ===
        self.print_header("7. ADMIN TESTS")
        
        passed, msg = await self.test_admin_login()
        self.test_result.add("Đăng nhập admin", passed, msg)
        
        passed, msg = await self.test_admin_dashboard()
        self.test_result.add("Dashboard admin", passed, msg)
        
        passed, msg = await self.test_admin_get_users()
        self.test_result.add("Lấy danh sách users", passed, msg)
        
        # === SUMMARY ===
        self.test_result.summary()

async def main():
    tester = APITester()
    try:
        await tester.run_all_tests()
    except Exception as e:
        print(f"\n{Colors.RED}❌ Lỗi: {e}{Colors.RESET}")
    finally:
        await tester.close()

if __name__ == "__main__":
    asyncio.run(main())