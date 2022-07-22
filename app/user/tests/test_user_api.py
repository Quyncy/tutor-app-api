"""
Test for the user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

# public test zb für registrierung
# private für authentifizierung

class PublicUserApiTest(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        # payload = Nutzdaten
        payload = {
            'email': 'test@example.com',
            'password':'testpass123',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL,payload)

        # Stellt fest, ob der client die Anfrage verstanden hat
        # falls ja müssten der status_code gleich sein
        self.asserEqual(res.status_code, status.HTTP_201_CREATED)

        # hole die Daten vom User. Hole aber nicht das passwort(aus sicherheitsgründen)
        # deshalb stelle sicher, dass 'password' im erhaltenen Objekt drin ist
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('passwort', res.data)


    def test_user_with_email_exists_error(self):
        """Test error returned if suer with email exists."""
        payload = {
            'email': 'test@example.com',
            'password':'testpass123',
            'name': 'Test name',
        }
        # == create_user(email='test@example.com', password='testpass123', name='Test name')
        # speicher in die Datenbank
        create_user(**payload)

        # CREATE_USER_URL = reverse('user:create')
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password':'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # ???
        self.assertEqual(res.status_code, status.HTTP_BAD_400_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
