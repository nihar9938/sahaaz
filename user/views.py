from django.shortcuts import render
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
import pyotp
from rest_framework.response import Response
from rest_framework.generics import (GenericAPIView)
from rest_framework.views import APIView
from .models import PhoneModel
import base64
from .utils import (ResponseInfo)
from utilities import message


# This class returns the string needed to generate the key


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "sahaaz"


EXPIRY_TIME = 50  # seconds


class VerifyPhoneNumberAPIVIEW(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = PhoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            PhoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = PhoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)
        print(OTP.now())
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        data = {
            "data":OTP.now(),
            "status": status.HTTP_200_OK,
            "error": None,
            "message": message.OTP_SENT
        }
        return Response(data)


    @staticmethod
    def post(request, phone):
        try:
            Mobile = PhoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.TOTP(key, interval = EXPIRY_TIME)
        if OTP.verify(request.data["otp"]):
            Mobile.isVerified = True
            Mobile.save()
            data = {
                "data": [],
                "status": status.HTTP_200_OK,
                "error": None,
                "message": message.OTP_SUCCESS
            }
            return Response(data)

        data = {
            "data": [],
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "otp",
            "message": message.OTP_FAILURE
        }
        return Response(data)
