import json
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from ..models import User as UserModel, UsageTypes, Usage
from ..serializers import UserSerializer, UsageSerializer



def api_authentication(self):
    self.user = User.objects.create_user(username='test', password='testpwd123')
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)


def api_authentication_staff(self):
    self.user = User.objects.create_user(username='admin', password='password123', is_staff=True)
    self.token = Token.objects.create(user=self.user)
    self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)


class GetAllUsersTest(APITestCase):
    '''Test module for GET all Users API'''

    def setUp(self):
        api_authentication(self)
        UserModel.objects.create(id=3, name='Casper')
        UserModel.objects.create(id=4, name='Muffin')

    def test_get_all_users(self):
        response = self.client.get(reverse('get_users'))
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewUserTest(APITestCase):
    '''Test module for POST new User API'''


    def setUp(self):
        api_authentication_staff(self)
        self.valid_payload = {
            'id': 5,
            'name': 'Musketeer'
        }
        self.invalid_payload = {
            'id': '',
            'name': 'Musketeer'
        }

    def test_create_valid_user(self):
        response = self.client.post(reverse('post_users'),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_user(self):
        response = self.client.post(reverse('post_users'),
                                data=json.dumps(self.invalid_payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllUsersUsageTest(APITestCase):
    def setUp(self):
        api_authentication(self)
        test_user = UserModel.objects.create(id=9, name='Evin')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        Usage.objects.create(id=51, user_id=test_user, usage_type_id=usagetype, amount=22.2)

    
    def test_get_all_users_usage(self):
        response = self.client.get(reverse('per_user_usage'))
        users = Usage.objects.all()
        serializer = UsageSerializer(users, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewUserUsageTest(APITestCase):
    def setUp(self):
        api_authentication(self)

        UserModel.objects.create(id=10, name='Eff')
        UserModel.objects.create(id=11, name='Jasmin')
        UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)

        self.valid_payload = {
            'id': 5,
            'user_id': 10,
            'usage_type_id': 102,
            'amount': 13.2
        }

        self.invalid_payload = {
            'id': 6,
            'user_id': '',
            'usage_type_id': 102,
            'amount': 13.2
        }
    
    def test_create_valid_user_usage(self):
        response = self.client.post(reverse('per_user_usage'),
                                data=json.dumps(self.valid_payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_user_usage(self):
        response = self.client.post(reverse('per_user_usage'),
                                data=json.dumps(self.invalid_payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class GetSingleUserUsage(APITestCase):
    def setUp(self):
        api_authentication_staff(self)

        user = UserModel.objects.create(id=6, name='Julius')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        self.usage = Usage.objects.create(id=51, user_id=user, usage_type_id=usagetype, amount=12.2)

    def test_get_valid_user_usage(self):
        response = self.client.get(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.user_id}))
        usage = Usage.objects.get(pk=self.usage.user_id)
        serializer = UsageSerializer(usage)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_valid_user_usage(self):
        response = self.client.get(reverse('get_delete_update_user_usage', kwargs={'pk': 45}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleUserTest(APITestCase):
    def setUp(self):
        api_authentication_staff(self)
    
        test_user = UserModel.objects.create(id=7, name='Caesar')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        self.usage = Usage.objects.create(id=52, user_id=test_user, usage_type_id=usagetype, amount=13.2)
    
        self.valid_payload = {
            'id': 52,
            'user_id': 7,
            'usage_type_id': 102,
            'amount': 14.5
        }

        self.invalid_payload = {
            'id': 52,
            'user_id': 7,
            'usage_type_id': 102,
            'amount': ''
        }
    
    def test_valid_update_user_usage(self):
        response = self.client.put(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.id}),
                                    data = json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_invalid_update_user_usage(self):
        response = self.client.put(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.id}),
                                    data = json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleUserTest(APITestCase):
    def setUp(self):
        api_authentication_staff(self)

        test_user = UserModel.objects.create(id=7, name='Caesar')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        self.usage = Usage.objects.create(id=53, user_id=test_user, usage_type_id=usagetype, amount=13.2)
    
    def test_valid_delete_user_usage(self):
        response = self.client.delete(reverse('get_delete_update_user_usage', kwargs={'pk': self.usage.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_delete_user_usage(self):
        response = self.client.delete(reverse('get_delete_update_user_usage', kwargs={'pk': 45}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetEachUsersUsageTest(APITestCase):
    def setUp(self):
        api_authentication(self)
    
        test_user = UserModel.objects.create(id=71, name='Muftak')
        usagetype = UsageTypes.objects.create(id=102, name='heating', unit='kwh', factor=3.892)
        self.usage = Usage.objects.create(id=55, user_id=test_user, usage_type_id=usagetype, amount=13.2)

        test_user = UserModel.objects.create(id=72, name='Lione')
        usagetype = UsageTypes.objects.create(id=100, name='electricity', unit='kwh', factor=1.5)
        self.usage = Usage.objects.create(id=56, user_id=test_user, usage_type_id=usagetype, amount=3.2)
    
    def test_get_each_users_usage(self):
        usage_obj = Usage.objects.get(user_id=self.usage.user_id)
        serializer = UsageSerializer(usage_obj)
        response = self.client.get(reverse('get_each_user_usage', kwargs={'userid': self.usage.user_id_id}))
        self.assertEqual(json.loads(json.dumps(response.data))['results'][0], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)