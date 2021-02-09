from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import MyTokenObtainPairView, Current_User_API, BlacklistTokenUpdateView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get_current_user/', Current_User_API.as_view(), name='current_user'),
    path('logout/', BlacklistTokenUpdateView.as_view(), name='blacklist'),

]
