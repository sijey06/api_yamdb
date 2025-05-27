from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet, signup, confirm_and_get_token

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', confirm_and_get_token, name='token'),
    path('v1/', include(router.urls)),
]
