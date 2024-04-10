from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("hospital/", include("hospital.urls")),
    path("admin/", admin.site.urls),
]
