from django.test import TestCase
from .models import Location, Accommodation, LocalizeAccommodation
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import Group, User


class LocationModelTests(TestCase):
    def test_valid_country_code(self):
        location = Location(
            id="1",
            title="Test Location",
            country_code="US",
            location_type="country"
        )
        location.clean()  # Validation should pass without errors
        self.assertEqual(location.country_code, "US")
    
    def test_invalid_country_code(self):
        location = Location(
            id="1",
            title="Invalid Location",
            country_code="XX",
            location_type="country"
        )
        with self.assertRaises(ValidationError):
            location.clean()
    
    def test_state_abbr_length(self):
        location = Location(
            id="2",
            title="State Test",
            state_abbr="CA",
            location_type="state"
        )
        location.clean()  # Should not raise errors
    
    def test_invalid_state_abbr_length(self):
        location = Location(
            id="3",
            title="Invalid State",
            state_abbr="LONG",
            location_type="state"
        )
        with self.assertRaises(ValidationError):
            location.clean()

class AccommodationModelTests(TestCase):
    def test_create_accommodation(self):
        location = Location.objects.create(
            id="1", title="Test Location", location_type="country"
        )
        accommodation = Accommodation.objects.create(
            id="A1",
            title="Test Accommodation",
            country_code="US",
            bedroom_count=3,
            review_score=4.5,
            usd_rate=120.50,
            location=location,
            center=Point(12.9716, 77.5946)
        )
        self.assertEqual(accommodation.title, "Test Accommodation")
        self.assertIsInstance(accommodation.center, Point)

    def test_invalid_accommodation_center(self):
        location = Location.objects.create(
            id="1", title="Test Location", location_type="country"
        )
        with self.assertRaises(ValueError):
            Accommodation.objects.create(
                id="A2",
                title="Invalid Accommodation",
                country_code="US",
                bedroom_count=3,
                usd_rate=150.00,
                location=location,
                center="Invalid Center"  # Invalid input
            )


class SignupViewTests(TestCase):
    
    def setUp(self):
        # Create a user for testing signup
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'testuser@example.com'
        
        # Create the first user
        self.existing_user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
    
    def test_signup_successful(self):
        # Send POST request with valid data (unique username)
        response = self.client.post(reverse('properties:signup'), {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        })

        
        # Check if the user was actually created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        # Check if the success message is displayed
        self.assertContains(response, "Your account has been created! You can now log in.")
    
    def test_signup_unsuccessful_duplicate_username(self):
        # Send POST request with a duplicate username
        response = self.client.post(reverse('properties:signup'), {
            'username': self.username,  # Use the existing username
            'password': 'newpassword',
            'email': 'anotheruser@example.com'
        })
        
        # Check if the form is not valid (should not be redirected)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        # Check if the error message for duplicate username is shown
        self.assertContains(response, "This username is already taken. Please choose a different one.")
        # Ensure no duplicate users were created
        self.assertEqual(User.objects.filter(username=self.username).count(), 1)

    

    def test_signup_unsuccessful_duplicate_email(self):
        # Send POST request with a duplicate email
        response = self.client.post(reverse('properties:signup'), {
            'username': 'newuser',  # A new username
            'password': 'newpassword',
            'email': self.email  # Use the existing email
        })
        
        # Check if the form is not valid (should not be redirected)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        # Check if the error message for duplicate email is shown
        self.assertContains(response, "This email is already taken. Please choose a different one.")
        # Ensure no duplicate emails were created
        self.assertEqual(User.objects.filter(email=self.email).count(), 1)


    def test_signup_unsuccessful_blank_username(self):
        # Try submitting with a blank username
        response = self.client.post(reverse('properties:signup'), {
            'username': '',  # Blank username
            'password': 'newpassword',
            'email': 'nousername@example.com'
        })
        
        # Check if the form is not valid (should not be redirected)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        # Check if the error message for blank username is shown
        self.assertContains(response, "This field is required.")
    
    def test_signup_unsuccessful_blank_password(self):
        # Try submitting with a blank password
        response = self.client.post(reverse('properties:signup'), {
            'username': 'anotheruser',
            'password': '',  # Blank password
            'email': 'no_password@example.com'
        })
        
        # Check if the form is not valid (should not be redirected)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        # Check if the error message for blank password is shown
        self.assertContains(response, "This field is required.")


    
    