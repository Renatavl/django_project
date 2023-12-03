from django.urls import path
from . import views

urlpatterns = [
    path("api/v1/hello-world-<int:variant_number>/", views.hello_world, name = "hello_world"),
]