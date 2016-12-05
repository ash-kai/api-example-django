from django.shortcuts import render, redirect
# Create your views here.
from . import authenticate, utility
import datetime, pytz
from models import Token

def index(request):
	if 'user' in request.session:
		# doc = authenticate.get_doctor(request.session['doctor'])
		token = Token.objects.get(pk = request.session['user'])
		appointments = authenticate.getAppointments(token.access_token)
		context = {
			"appointments": appointments
		}
		return render(request, "dashboard.html", context)

	context = {
		"client_id": authenticate.client_id,
	}
	return render(request, "index.html", context)

def authorize(request):
	print "the code is %s" %(request.GET.get("code"))
	authToken = authenticate.getToken(request.GET.get("code",None))
	expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=authToken['expires_in'])
	print "Expires Timestamp %s" %expires_timestamp
	token = Token.objects.create(
		access_token = authToken['access_token'], 
		refresh_token = authToken['refresh_token'], 
		expire_timestamp = expires_timestamp)
	token.save()
	request.session['user'] = token.pk;
	return redirect('/')

def profile(request):
	if 'user' in request.session:
		token = Token.objects.get(pk = request.session['user'])
		docInfo = authenticate.getDoctorInfo(token.access_token)
		print docInfo
		context = {
		'profile' : docInfo,
		}
		return render(request, "profile.html", context)
	else:
		print "its not present"
		return redirect('/')
