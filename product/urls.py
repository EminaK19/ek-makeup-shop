from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoriesList, CompanyList, ProductViewSet, ReviewCreate, RatingSelect

router = DefaultRouter()
router.register('', ProductViewSet)


urlpatterns = [
    path('categories/', CategoriesList.as_view()),
    path('brands/', CompanyList.as_view()),
    path('', include(router.urls)),
    path('review/create/', ReviewCreate.as_view()),
    path('rating/select/', RatingSelect.as_view()),
]