import requests
import datetime
from django.conf import settings
from config import *
from django.utils import timezone

# client_id = "uXIJz6c0WeIW1QOJPQuRjwEyEywRB5aVR1dRT7mp"
# client_secret = "eVeX00W1UD1EyrJlk1HNil5YQn5CeVfSxeVtscH8b8RRu0O3I2XKTLEbj57jfwhIr0XFmZOH0ZJYl78BLsRwlNqxWKjto9nNigpN6aFmqnqHp1jtKapYJq7VqE10xEEd"

def get_token(code):
	data = {
		"grant_type":    "authorization_code",
		"client_id":     client_id,
		"client_secret": client_secret,
		"code":          code,
		"redirect_uri":  "http://127.0.0.1:8000/authorize",
	}
	response = requests.post("https://drchrono.com/o/token/", data=data)
	response.raise_for_status()
	return response.json()
	
def refresh_token(refresh_token):
	data = {
		"grant_type":    "refresh_token",
		"client_id":     client_id,
		"client_secret": client_secret,
		'refresh_token': refresh_token,
	}
	response = requests.post("https://drchrono.com/o/token/", data=data)
	response.raise_for_status()
	return response.json()

def recharge_token(func):
	def recharge(*args, **kwargs):
		token = args[0]
		if token.expire_timestamp < timezone.now():
			new_tokens = refresh_token(token.refresh_token)
			token.access_token = new_tokens["access_token"]
			token.refresh_token = new_tokens["refresh_token"]
			token.expire_timestamp = datetime.datetime.now() +\
					datetime.timedelta(seconds=new_tokens["expires_in"])
			token.save()
		return func(*args, **kwargs)
	return recharge

def get_api(url, payload):
	data = payload['data']
	headers = get_auth_header(payload['access_token'])
	response = requests.get(url, params=data, headers=headers)
	response.raise_for_status()
	return response

def patch_api(url, payload):
	data = payload['data']
	headers = get_auth_header(payload['access_token'])
	response = requests.patch(url, data=data, headers=headers)
	print response
	response.raise_for_status()
	return response

@recharge_token
def getAppointments(token):
	data = {
	"date" : datetime.datetime.today().isoformat(),
	}
	payload = {
	"access_token": token.access_token,
	"data": data,
	}
	return get_api('https://drchrono.com/api/appointments', payload)

@recharge_token
def getAppointmentsPerPatient(token, patientId):
	data = {
	"date" : datetime.datetime.now().date(),
	"patient" : patientId,
	}
	payload = {
	"access_token": token.access_token,
	"data": data,
	}
	return get_api('https://drchrono.com/api/appointments', payload)

@recharge_token
def getDoctorInfo(token):
	payload = {
	"access_token": token.access_token,
	"data": {},
	}
	return get_api('https://drchrono.com/api/users/current', payload)

@recharge_token
def getPatientInfo(token, firstName, lastName):
	data = {
	"first_name" : firstName,
	"last_name" : lastName,
	}
	payload = {
	"access_token":token.access_token,
	"data":data,
	}
	return get_api('https://drchrono.com/api/patients', payload)

@recharge_token
def updatePatientAppointmentData(token, appointmentId, status):
	print token.access_token, appointmentId, status
	data = {
	"status" : status
	}
	payload={
	'access_token':token.access_token,
	'data':data,
	}
	return patch_api('https://drchrono.com/api/appointments/{0}'.format(appointmentId), payload)

@recharge_token
def updatePatientDemographicInfo(token, patientId, data):
	payload={
	'access_token':token.access_token,
	'data':data,
	}
	return patch_api('https://drchrono.com/api/patients/{0}'.format(patientId), payload)

def get_auth_header(access_token):
	return {'Authorization': 'Bearer {0}'.format(access_token)}

