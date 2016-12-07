from django.db import models

# Create your models here.
class Token(models.Model):
	access_token = models.CharField(max_length = 200)
	refresh_token = models.CharField(max_length = 200)
	expire_timestamp = models.DateTimeField()

class Appointment(models.Model):
	appointmentId = models.CharField(max_length=200)
	checkIn = models.DateTimeField()
	scheduled_time = models.DateTimeField(null=True)
	inSession = models.DateTimeField(null=True)
