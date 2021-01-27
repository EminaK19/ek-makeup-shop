from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, ActivationView, \
    LoginView, LogoutView, ProfileViewSet


router = DefaultRouter()
router.register('', ProfileViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', include(router.urls)),

    # path('profile/<int:pk>/', ProfileViewSet.as_view({
    #     'get': 'retrieve',
    #     'patch': 'partial_update',
    #     'put': 'update'
    #     }))
]
