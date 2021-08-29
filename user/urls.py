from django.contrib import admin
from django.urls import path
from .views import (VerifyPhoneNumberAPIVIEW)
urlpatterns = [
    path("verifyPhone/<phone>/", VerifyPhoneNumberAPIVIEW.as_view(), name="verify phone number"),
]
