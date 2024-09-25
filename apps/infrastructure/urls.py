from django.urls import path

from . import views

app_name = "Infrastructure"

urlpatterns = [
    # Location
    path('location/', views.location, name="location_home"),
    path('location/create/', views.location_create, name="location_create"),
    path('location/<str:locationId>/update/', views.location_update, name="location_update"),
    path('location/<str:locationId>/delete/', views.location_delete, name="location_delete"),

    # Category
    path('category/', views.category, name="category_home"),
    path('category/create/', views.category_create, name="category_create"),
    path('category/<str:categoryId>/update/', views.category_update, name="category_update"),
    path('category/<str:categoryId>/delete/', views.category_delete, name="category_delete"),

    # Devices
    path('device/', views.device, name="device_home"),
    path('device/create/', views.device_create, name="device_create"),
    path('device/<str:deviceId>/update/', views.device_update, name="device_update"),
    path('device/<str:deviceId>/delete/', views.device_delete, name="device_delete"),
]
