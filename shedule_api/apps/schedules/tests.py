from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Schedule, TimeSlot



class ScheduleModelTest(TestCase):
        
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.schedule = Schedule.objects.create(
            name='Test Schedule',
            description='Test Description',
            owner=self.user
        )

    def test_schedule_creation(self):
        
        self.assertEqual(self.schedule.name, 'Test Schedule')
        self.assertEqual(self.schedule.description, 'Test Description')
        self.assertEqual(self.schedule.owner, self.user)
        self.assertTrue(self.schedule.is_active)

    def test_schedule_str_method(self):
        
        expected = f"{self.schedule.name} - {self.user.username}"
        self.assertEqual(str(self.schedule), expected)

    def test_soft_delete(self):
        
        self.schedule.soft_delete()
        self.assertFalse(self.schedule.is_active)        
        
        self.assertEqual(Schedule.objects.count(), 0)        
        
        self.assertEqual(Schedule.all_objects.count(), 1)

    def test_restore(self):
        
        self.schedule.soft_delete()
        self.schedule.restore()
        self.assertTrue(self.schedule.is_active)
        self.assertEqual(Schedule.objects.count(), 1)


class TimeSlotModelTest(TestCase):    
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.schedule = Schedule.objects.create(
            name='Test Schedule',
            owner=self.user
        )
        self.time_slot = TimeSlot.objects.create(
            schedule=self.schedule,
            day_of_week='monday',
            start_time='09:00',
            end_time='17:00',
            ids=[1, 2, 3]
        )

    def test_time_slot_creation(self):
        
        self.assertEqual(self.time_slot.schedule, self.schedule)
        self.assertEqual(self.time_slot.day_of_week, 'monday')
        self.assertEqual(self.time_slot.ids, [1, 2, 3])

    def test_time_slot_validation_start_before_end(self):
       
        with self.assertRaises(Exception):
            TimeSlot.objects.create(
                schedule=self.schedule,
                day_of_week='tuesday',
                start_time='17:00',
                end_time='09:00',
                ids=[1, 2]
            )

    def test_time_slot_str_method(self):
        
        expected = f"{self.schedule.name} - monday (09:00:00-17:00:00)"
        self.assertEqual(str(self.time_slot), expected)


class ScheduleAPITest(APITestCase):    
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )        
        
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.schedule_data = {
            'name': 'Test Schedule',
            'description': 'Test Description',
            'schedule': {
                'monday': [
                    {
                        'start': '09:00',
                        'stop': '17:00',
                        'ids': [1, 2, 3]
                    }
                ],
                'tuesday': [
                    {
                        'start': '10:00',
                        'stop': '18:00',
                        'ids': [4, 5, 6]
                    }
                ]
            }
        }

    def test_create_schedule_authenticated(self):
        
        url = reverse('schedules:schedule-list-create')
        response = self.client.post(url, self.schedule_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Schedule')
        self.assertEqual(response.data['owner'], 'testuser')        
        
        schedule = Schedule.objects.get(name='Test Schedule')
        self.assertEqual(schedule.time_slots.count(), 2)

    def test_create_schedule_unauthenticated(self):
       
        self.client.credentials() 
        url = reverse('schedules:schedule-list-create')
        response = self.client.post(url, self.schedule_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_schedules(self):        
        
        Schedule.objects.create(name='User Schedule', owner=self.user)
        Schedule.objects.create(name='Other Schedule', owner=self.other_user)
        
        url = reverse('schedules:schedule-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'User Schedule')

    def test_retrieve_schedule(self):
        
        schedule = Schedule.objects.create(name='Test Schedule', owner=self.user)
        TimeSlot.objects.create(
            schedule=schedule,
            day_of_week='monday',
            start_time='09:00',
            end_time='17:00',
            ids=[1, 2, 3]
        )
        
        url = reverse('schedules:schedule-detail', kwargs={'id': schedule.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Schedule')
        self.assertIn('schedule', response.data)
        self.assertIn('monday', response.data['schedule'])

    def test_update_schedule(self):
        
        schedule = Schedule.objects.create(name='Original Schedule', owner=self.user)
        
        update_data = {
            'name': 'Updated Schedule',
            'description': 'Updated Description',
            'schedule': {
                'wednesday': [
                    {
                        'start': '08:00',
                        'stop': '16:00',
                        'ids': [7, 8, 9]
                    }
                ]
            }
        }
        
        url = reverse('schedules:schedule-detail', kwargs={'id': schedule.id})
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Schedule')        
        
        updated_schedule = Schedule.objects.get(id=schedule.id)
        self.assertEqual(updated_schedule.time_slots.count(), 1)
        self.assertEqual(updated_schedule.time_slots.first().day_of_week, 'wednesday')

    def test_delete_schedule(self):
        
        schedule = Schedule.objects.create(name='Test Schedule', owner=self.user)
        
        url = reverse('schedules:schedule-detail', kwargs={'id': schedule.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.count(), 0)

    def test_cannot_access_other_user_schedule(self):
        
        other_schedule = Schedule.objects.create(name='Other Schedule', owner=self.other_user)
        
        url = reverse('schedules:schedule-detail', kwargs={'id': other_schedule.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_protected_endpoint(self):
       
        url = reverse('schedules:protected-endpoint')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['user'], 'testuser')

    def test_schedule_statistics(self):
       
        schedule = Schedule.objects.create(name='Test Schedule', owner=self.user)
        TimeSlot.objects.create(
            schedule=schedule,
            day_of_week='monday',
            start_time='09:00',
            end_time='17:00',
            ids=[1, 2, 3]
        )
        
        url = reverse('schedules:schedule-statistics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_schedules'], 1)
        self.assertEqual(response.data['total_time_slots'], 1)
        self.assertEqual(response.data['schedules_by_day']['monday'], 1)

    def test_invalid_schedule_data(self):
      
        invalid_data = {
            'name': 'Test Schedule',
            'schedule': {
                'monday': [
                    {
                        'start': '17:00',  
                        'stop': '09:00',
                        'ids': [1, 2, 3]
                    }
                ]
            }
        }
        
        url = reverse('schedules:schedule-list-create')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_ids_validation(self):
        
        invalid_data = {
            'name': 'Test Schedule',
            'schedule': {
                'monday': [
                    {
                        'start': '09:00',
                        'stop': '17:00',
                        'ids': []  
                    }
                ]
            }
        }
        
        url = reverse('schedules:schedule-list-create')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_ids_validation(self):
        
        invalid_data = {
            'name': 'Test Schedule',
            'schedule': {
                'monday': [
                    {
                        'start': '09:00',
                        'stop': '17:00',
                        'ids': [-1, 0, 'invalid']  
                    }
                ]
            }
        }
        
        url = reverse('schedules:schedule-list-create')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)