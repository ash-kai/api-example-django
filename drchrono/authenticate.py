import requests
import datetime
#To connect to drChrono api

client_id = "uXIJz6c0WeIW1QOJPQuRjwEyEywRB5aVR1dRT7mp"
client_secret = "eVeX00W1UD1EyrJlk1HNil5YQn5CeVfSxeVtscH8b8RRu0O3I2XKTLEbj57jfwhIr0XFmZOH0ZJYl78BLsRwlNqxWKjto9nNigpN6aFmqnqHp1jtKapYJq7VqE10xEEd"

def getToken(code):
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
	#to obtain access token and refresh token

def refreshToken(refresh_token):
	data = {
		"grant_type":    "refresh_token",
		"client_id":     client_id,
		"client_secret": client_secret,
		'refresh_token': refresh_token,
	}
	response = requests.post("https://drchrono.com/o/token/", data=data)
	response.raise_for_status()
	return response.json()
	#To obtain new access token after the previous token expires

def getAppointments(access_token):
	data = {
	"date" : datetime.datetime.now().date(),
	}
	headers = get_auth_header(access_token)
	response = requests.get('https://drchrono.com/api/appointments', params=data, headers=headers)
	response.raise_for_status()
	result = response.json()
	print len(result['results'])
	return result
	# Get todays appointments for the doctor

def getDoctorInfo(access_token):
	headers = get_auth_header(access_token)
	response = requests.get('https://drchrono.com/api/users/current', headers=headers)
	response.raise_for_status()
	data = response.json()
	print data
	# get resepective Doctor's info

def getPatientInfo(parameter):
	pass
	#get respective patients info

def get_auth_header(access_token):
    return {'Authorization': 'Bearer {0}'.format(access_token)}

