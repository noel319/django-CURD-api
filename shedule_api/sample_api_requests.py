import requests
import json

BASE_URL = "http://localhost:8000"

class ScheduleAPITester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.user_data = None

    def register_user(self):
        
        url = f"{self.base_url}/api/v1/auth/register/"
        data = {
            "username": "testuser123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
        
        response = requests.post(url, json=data)
        print(f"Register User: {response.status_code}")
        if response.status_code == 201:
            print(f"User created: {response.json()}")
        else:
            print(f"Error: {response.json()}")
        return response

    def login_user(self):
        
        url = f"{self.base_url}/api/v1/auth/login/"
        data = {
            "username": "testuser123",
            "password": "testpass123"
        }
        
        response = requests.post(url, json=data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access']
            self.refresh_token = data['refresh']
            self.user_data = data['user']
            print(f"Login successful for user: {self.user_data['username']}")
        else:
            print(f"Login failed: {response.json()}")
        return response

    def get_headers(self):
        
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def test_protected_endpoint(self):
        
        url = f"{self.base_url}/api/v1/schedules/protected/"
        response = requests.get(url, headers=self.get_headers())
        print(f"Protected Endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        return response

    def create_schedule(self):
        
        url = f"{self.base_url}/api/v1/schedules/"
        data = {
            "name": "Work Schedule",
            "description": "My weekly work schedule",
            "schedule": {
                "monday": [
                    {
                        "start": "09:00",
                        "stop": "17:00",
                        "ids": [1, 2, 3]
                    },
                    {
                        "start": "18:00",
                        "stop": "20:00",
                        "ids": [4, 5]
                    }
                ],
                "tuesday": [
                    {
                        "start": "10:00",
                        "stop": "18:00",
                        "ids": [6, 7, 8, 9]
                    }
                ],
                "wednesday": [],
                "thursday": [
                    {
                        "start": "08:00",
                        "stop": "16:00",
                        "ids": [10, 11, 12]
                    }
                ],
                "friday": [
                    {
                        "start": "09:00",
                        "stop": "15:00",
                        "ids": [13, 14]
                    }
                ],
                "saturday": [],
                "sunday": [
                    {
                        "start": "14:00",
                        "stop": "18:00",
                        "ids": [15, 16, 17]
                    }
                ]
            }
        }
        
        response = requests.post(url, json=data, headers=self.get_headers())
        print(f"Create Schedule: {response.status_code}")
        if response.status_code == 201:
            schedule_data = response.json()
            print(f"Schedule created with ID: {schedule_data['id']}")
            return schedule_data
        else:
            print(f"Error creating schedule: {response.json()}")
        return None

    def list_schedules(self):
        
        url = f"{self.base_url}/api/v1/schedules/"
        response = requests.get(url, headers=self.get_headers())
        print(f"List Schedules: {response.status_code}")
        if response.status_code == 200:
            schedules = response.json()
            print(f"Found {schedules['count']} schedules")
            for schedule in schedules['results']:
                print(f"  - {schedule['name']} (ID: {schedule['id']})")
            return schedules
        return None

    def get_schedule(self, schedule_id):
        
        url = f"{self.base_url}/api/v1/schedules/{schedule_id}/"
        response = requests.get(url, headers=self.get_headers())
        print(f"Get Schedule: {response.status_code}")
        if response.status_code == 200:
            schedule = response.json()
            print(f"Retrieved schedule: {schedule['name']}")
            return schedule
        return None

    def update_schedule(self, schedule_id):
        
        url = f"{self.base_url}/api/v1/schedules/{schedule_id}/"
        data = {
            "name": "Updated Work Schedule",
            "description": "Updated weekly work schedule",
            "schedule": {
                "monday": [
                    {
                        "start": "08:00",
                        "stop": "16:00",
                        "ids": [1, 2, 3, 4]
                    }
                ],
                "tuesday": [
                    {
                        "start": "09:00",
                        "stop": "17:00",
                        "ids": [5, 6, 7]
                    }
                ],
                "wednesday": [
                    {
                        "start": "10:00",
                        "stop": "18:00",
                        "ids": [8, 9]
                    }
                ],
                "thursday": [],
                "friday": [],
                "saturday": [],
                "sunday": []
            }
        }
        
        response = requests.put(url, json=data, headers=self.get_headers())
        print(f"Update Schedule: {response.status_code}")
        if response.status_code == 200:
            print("Schedule updated successfully")
            return response.json()
        return None

    def get_statistics(self):
        
        url = f"{self.base_url}/api/v1/schedules/statistics/"
        response = requests.get(url, headers=self.get_headers())
        print(f"Get Statistics: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"Statistics: {json.dumps(stats, indent=2)}")
            return stats
        return None

    def delete_schedule(self, schedule_id):
        
        url = f"{self.base_url}/api/v1/schedules/{schedule_id}/"
        response = requests.delete(url, headers=self.get_headers())
        print(f"Delete Schedule: {response.status_code}")
        if response.status_code == 204:
            print("Schedule deleted successfully")
        return response

    def run_full_test(self):
        
        print("=== Starting API Test ===\n")
        
        print("1. Registering user...")
        self.register_user()
        print()        
        
        print("2. Logging in...")
        login_response = self.login_user()
        if login_response.status_code != 200:
            print("Login failed, stopping test")
            return
        print()        
        
        print("3. Testing protected endpoint...")
        self.test_protected_endpoint()
        print()        
        
        print("4. Creating schedule...")
        schedule = self.create_schedule()
        if not schedule:
            print("Failed to create schedule, stopping test")
            return
        schedule_id = schedule['id']
        print()        
       
        print("5. Listing schedules...")
        self.list_schedules()
        print()        
       
        print("6. Getting specific schedule...")
        self.get_schedule(schedule_id)
        print()        
        
        print("7. Getting statistics...")
        self.get_statistics()
        print()        
        
        print("8. Updating schedule...")
        self.update_schedule(schedule_id)
        print()        
     
        print("9. Getting updated schedule...")
        self.get_schedule(schedule_id)
        print()        
       
        print("10. Deleting schedule...")
        self.delete_schedule(schedule_id)
        print()
        
        print("=== API Test Complete ===")


def test_error_cases():
    """Test various error cases"""
    print("\n=== Testing Error Cases ===\n")    
   
    print("1. Testing without authentication...")
    response = requests.get(f"{BASE_URL}/api/v1/schedules/")
    print(f"Unauthenticated request: {response.status_code}")
    print()    
    
    print("2. Testing invalid login...")
    response = requests.post(f"{BASE_URL}/api/v1/auth/login/", json={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    print(f"Invalid login: {response.status_code}")
    print()    
    
    print("3. Testing invalid schedule data...")
    tester = ScheduleAPITester()
    tester.login_user()  
    
    invalid_data = {
        "name": "Invalid Schedule",
        "schedule": {
            "monday": [
                {
                    "start": "17:00", 
                    "stop": "09:00",
                    "ids": [1, 2, 3]
                }
            ],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": []
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/schedules/",
        json=invalid_data,
        headers=tester.get_headers()
    )
    print(f"Invalid schedule data: {response.status_code}")
    if response.status_code != 201:
        print(f"Error response: {response.json()}")


if __name__ == "__main__":
    
    tester = ScheduleAPITester()
    tester.run_full_test()    
    
    test_error_cases()
    
    print("\n=== All Tests Complete ===")
    print(f"Swagger documentation available at: {BASE_URL}/")
    print(f"Admin interface available at: {BASE_URL}/admin/")