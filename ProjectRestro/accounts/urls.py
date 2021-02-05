from django.urls import path
from accounts.views import (
    signup,
    loginpage,
    logoutuser,
)


urlpatterns = [
    path('register/', signup, name="signup"),

    path('login/', loginpage, name="login"),

    path('logout/', logoutuser, name='logout')
] 