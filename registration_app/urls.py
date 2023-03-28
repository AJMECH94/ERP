from django.urls import path,include
from rest_framework.routers import DefaultRouter
from registration_app.views import UserRegistrationAPI,AddDepartmentView,UserLoiginAPI,UserChangePasswordView

router = DefaultRouter()
router.register(r'sign-up', UserRegistrationAPI)

urlpatterns = [
    # path('sign-up/',UserRegistrationAPI.as_view(),name='sign_up'),
    path('add-department/',AddDepartmentView.as_view(),name='add_department'),
    path('login/',UserLoiginAPI.as_view(),name='login'),
    path('', include(router.urls)),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
]
