from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from automotivePartsManager.views import CSVUploadView, PartViewSet, CarModelViewSet, PartCarModelViewSet, RegisterUserView, UserManagementViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Sistema de Gerenciamento de Peças Automotivas",
      default_version='v1',
      description="Documentação da API para o teste técnico da Hubbi.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="flavioalexandrework@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[],
)

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
    path('upload-csv/', CSVUploadView.as_view(), name='upload_csv'),
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
