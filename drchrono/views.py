from django.shortcuts import render, redirect
# Create your views here.
from . import authenticate, utility
import datetime, pytz

def index(request):
	if 'access_token' in request.session:
		# doc = authenticate.get_doctor(request.session['doctor'])
		appointments = authenticate.getAppointments(request.session['access_token'])
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
	token = authenticate.getToken(request.GET.get("code",None))
	print token
	expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=token['expires_in'])
	print expires_timestamp
	request.session['access_token'] = token["access_token"]
	request.session['refresh_token'] = token["refresh_token"]
	#request.session['expires'] = expires_timestamp
	context = {
	"token" : token,
	}
	return render(request, "dashboard.html", context)

def profile(request):
	if 'access_token' in request.session:
		docInfo = authenticate.getDoctorInfo(request.session['access_token'])
		print docInfo
		context = {
		'profile' : docInfo,
		}
		return render(request, "profile.html", context)
	else:
		print "its not present"
		return redirect('/')
