from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clothes import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'clothes'

urlpatterns = [
    path('', include(router.urls))
]
