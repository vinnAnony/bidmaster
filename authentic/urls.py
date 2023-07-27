from django.urls import path
from .views import *

app_name = "authentic"
urlpatterns = [
    path("login/", log_in, name="log_in"),
    path("signup/", sign_up, name="sign_up"),
]
