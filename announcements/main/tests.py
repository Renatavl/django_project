from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Announcement

class AnnouncementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.announcement = Announcement.objects.create(
            subject='Test Subject',
            title='Test Title',
            content='Test Content',
            access='public',
            user_profile=self.user
        )

    def test_get_user_announcement_list(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('get_user_announcement'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title')

    def test_get_public_announcements(self):
        response = self.client.get(reverse('get_public_announcements'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title')

    def test_get_announcement_by_id(self):
        response = self.client.get(reverse('get_announcement_by_id', args=[self.announcement.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title')

    def test_get_announcement_by_id_Error(self):
        response = self.client.get(reverse('get_announcement_by_id', args=[100000]))
        self.assertNotContains(response, 'Test Title')

    def test_create_announcement(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('create_announcement'), {'subject': 'New Subject', 'title': 'New Title', 'content': 'New Content', 'access': 'public'})
        self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for redirect
        new_announcement = Announcement.objects.get(title='New Title')
        self.assertEqual(new_announcement.content, 'New Content')

   

    def test_delete_announcement(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_announcement', args=[self.announcement.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Announcement.DoesNotExist):
            Announcement.objects.get(id=self.announcement.id)

    def test_register(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'password1': 'newpas214','password2': 'newpas214'})
        self.assertEqual(response.status_code, 302)
        new_user = get_user_model().objects.get(username='newuser')
        self.assertIsNotNone(new_user)

    def test_user_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_user_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
