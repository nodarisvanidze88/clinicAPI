from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCreate, LoginUser,CustomUserViewset,AppointmentViewset,AvailabilityViewset,DoctorViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewset)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewset)
router.register(r'availabilities', AvailabilityViewset)
urlpatterns = [
    path('register/', UserCreate.as_view(), name='account-create'),
    path('login/', LoginUser.as_view(), name='account-login'),
    path('', include(router.urls))
]
