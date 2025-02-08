from django.urls import path, include
from rest_framework.routers import DefaultRouter
from automotivePartsManager.views import PartViewSet, CarModelViewSet, PartCarModelViewSet, RegisterUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'parts', PartViewSet, basename='part')
router.register(r'carmodels', CarModelViewSet, basename='carmodel')
router.register(r'part-carmodel', PartCarModelViewSet, basename='partcarmodel')

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
