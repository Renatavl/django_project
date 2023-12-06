from django.urls import path
from .views import get_user_announcement_list, create_announcement, get_public_announcements, get_local_announcements, get_announcement_by_id, update_announcement, delete_announcement, register, user_login, home, user_logout

urlpatterns = [
    path('announcements/public', get_public_announcements, name='get_public_announcements'),
    path('announcements/local', get_local_announcements, name='get_local_announcements'),
    path('announcements/create', create_announcement, name='create_announcement'),
    path('announcements/user/',  get_user_announcement_list, name='get_user_announcement'),
    path('announcement/<int:id>/update', update_announcement, name='update_announcement'),
    path('announcement/<int:id>/delete', delete_announcement, name='delete_announcement'),
    path('announcement/<int:id>/', get_announcement_by_id, name='get_announcement_by_id'),
   
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
]



    


