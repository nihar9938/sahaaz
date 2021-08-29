from django.db import models

# Create your models here.
# this model Stores the data of the Phones Verified


class PhoneModel(models.Model):
    Mobile = models.BigIntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)   # For HOTP Verification

    def __str__(self):
        return str(self.Mobile)
