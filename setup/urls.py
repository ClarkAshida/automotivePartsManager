from django.urls import path, include
from rest_framework.routers import DefaultRouter
from automotivePartsManager.views import PartViewSet, CarModelViewSet, PartCarModelViewSet, RegisterUserView, UserManagementViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'parts', PartViewSet, basename='part')
router.register(r'carmodels', CarModelViewSet, basename='carmodel')
router.register(r'part-carmodel', PartCarModelViewSet, basename='partcarmodel')
router.register(r'users', UserManagementViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('part-carmodel/associate/', PartCarModelViewSet.as_view({'post': 'associate_parts_to_car_models'}), name='associate-parts-to-car-models'),
    path('part-carmodel/parts-by-car-model/', PartCarModelViewSet.as_view({'get': 'get_parts_by_car_model'}), name='get-parts-by-car-model'),
    path('part-carmodel/car-models-by-part/', PartCarModelViewSet.as_view({'get': 'get_car_models_by_part'}), name='get-car-models-by-part'),
]
