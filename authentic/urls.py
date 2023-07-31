from django.urls import path
from .views import *

app_name = "authentic"
urlpatterns = [
    path("accounts/signup/", sign_up, name="sign_up"),
    path("accounts/login/", log_in, name="log_in"),
    path("logout/", log_out, name="log_out"),
]
