from account.models import User, Profile
from account.forms import ProfileAndUserRegistrationForm
from django.test import TestCase

class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='anotherusername@gmail.com',
            password='testpassword'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            first_name='test',
            last_name='user',
            dni='12345678A',
            date_of_birth='1990-01-01'
        )

    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='anotherusername@gmail.com',
            password='testpassword'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'anotherusername@gmail.com')
        self.assertTrue(user.check_password('testpassword'))

        self.assertIsInstance(user, User)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        self.assertEqual(user, User.objects.get(username='testuser'))

    def test_profile_creation(self):
        user, profile = self.user, self.profile

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.dni, '12345678A')
        self.assertEqual(profile.date_of_birth, '1990-01-01')
        self.assertEqual(profile.courses.all(), [])

    def test_profile_and_user_relation(self):
        user, profile = self.user, self.profile

        self.assertEqual(profile.user.get_full_name(), 'test user')
        self.assertEqual(profile.user.email, 'anotherusername@gmail.com')
        self.assertEqual(profile.user.username, 'testuser')

        self.assertEqual(profile.user, user)
        self.assertEqual(user.profile, profile)

        self.assertEqual(user.profile.courses, profile.courses)


    def test_profile_registration_form(self):
        """
        Tests all clean checks implemented in the modelForm assosiated with profile and user creation.
        """
        valid_form_data = {
            'first_name': 'test',
            'last_name': 'user',
            'dni': '12345678A',
            'date_of_birth': '1990-01-01',
            'email': 'ppistola@etec.uba.ar'
        }

        form = ProfileAndUserRegistrationForm(data=valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertEqual(form.non_field_errors(), [])

        valid_user = form.create_user()

        self.assertIsInstance(valid_user, User)
        self.assertFalse(valid_user.is_active)
        self.assertEqual(valid_user.username, 'ppistola')

