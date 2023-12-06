from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Announcement

# Створимо окремий клас для адміністрування вашого розширеного UserProfile
class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'location', 'is_staff', 'is_active',)
    list_editable = ( 'location', 'is_active')  

    search_fields = ('username', 'email', 'location',)
    list_filter = ('is_staff', 'is_active', 'location',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display_links = ('username',)
# Реєструємо UserProfile з нашим адмін-класом
admin.site.register(UserProfile, UserProfileAdmin)

# Реєструємо Announcement
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'title', 'content', 'access', 'location', 'user_profile', 'create_date')
    list_editable = ('subject', 'title',  'access', 'location')  
    search_fields = ('subject', 'title', 'content', 'location', 'user_profile__username')
    list_filter = ('access', 'location', 'user_profile')
    ordering = ('-create_date',)

    # Додаємо 'id' до list_display_links
    list_display_links = ('id',)

admin.site.register(Announcement, AnnouncementAdmin)
