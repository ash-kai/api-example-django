from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect
from . import auth, utility
import datetime, pytz
from models import Token, Appointment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

def loginUser(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				messages.success(request, "Login successful")
				return HttpResponseRedirect('/')
			else:
				messages.error(request, "Your account is disabled")
				return redirect('/')
		else:
			messages.error(request, "Invalid login details for {0}".format(username))
			return redirect('/')
	else:
		return render(request, 'login.html', {})

def index(request):
	# if 'user' in request.session:
	# 	# doc = auth.get_doctor(request.session['doctor'])
	# 	token = Token.objects.get(pk = request.session['user'])
	# 	appointments = auth.getAppointments(token.access_token)
	# 	context = {
	# 		"appointments": appointments
	# 	}
	# 	return render(request, "dashboard.html", context)
	# else
	if request.session.get('user',False):
		pass
	else:
		try:
			obj = Token.objects.latest('id')
		except Token.DoesNotExist:
			obj = None
		if obj is None:
			print "No token present"
		else:
			print "Token is present"
			request.session['user'] = obj.id
	if 'user' in request.session:
		return redirect("dashboard")
	else:
		context = RequestContext(request, {
			"client_id": auth.client_id,
		})
		return render_to_response("index.html", context_instance=context)
		
@login_required(login_url='login')
def dashboard(request):
	if 'user' in request.session:
		try:
			token = Token.objects.get(pk = request.session['user'])
		except Token.DoesNotExist:
			del request.session['user']
			return redirect('/')
		averageTime = divmod(utility.getAverageTime(),60)[0]
		appointments = auth.getAppointments(token)
		context = RequestContext(request, {
			"appointments": appointments.json()['results'],
			"averageTime" : averageTime,
		})
		return render_to_response("dashboard.html", context_instance=context)
	else:
		return redirect('/')

def notActive(request):
	return render(request, "notActive.html", {})

def home(request):
	if request.session.get('user',False):
		pass
	else:
		try:
			obj = Token.objects.latest('id')
		except Token.DoesNotExist:
			obj = None
		if obj is None:
			print "No token present"
		else:
			print "Token is present"
			request.session['user'] = obj.id
	if 'user' in request.session:
		print request.user
		try:
			token = Token.objects.get(pk = request.session['user'])
		except Token.DoesNotExist:
			del request.session['user']
			return redirect('notActive')
		appointments = auth.getAppointments(token)
		context = RequestContext(request, {
			"appointments": appointments.json()['results']
		})
		return render_to_response("dashboard.html", context_instance=context)
	else:
		return redirect("notActive")

def authorize(request):
	print "the code is %s" %(request.GET.get("code"))
	authToken = auth.get_token(request.GET.get("code",None))
	expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=authToken['expires_in'])
	print "Expires Timestamp %s" %expires_timestamp
	token = Token.objects.create(
		access_token = authToken['access_token'], 
		refresh_token = authToken['refresh_token'], 
		expire_timestamp = expires_timestamp)
	token.save()
	request.session['user'] = token.pk;
	return redirect("home")

@login_required(login_url='login')
def profile(request):
	if 'user' in request.session:
		token = Token.objects.get(pk = request.session['user'])
		docInfo = auth.getDoctorInfo(token)
		print docInfo.json()
		context = {
		'profile' : docInfo.json(),
		}
		return render(request, "profile.html", context)
	else:
		print "its not present"
		return redirect('/')

def validatePatient(request):
	if request.method=='POST':
		token = Token.objects.get(pk = request.session['user'])
		firstName = request.POST['firstName']
		lastName = request.POST['lastName']

		patient = auth.getPatientInfo(token, firstName, lastName)
		if patient.status_code!=200:
			return HttpResponseNotFound("No records found for Patient: {0}".format(firstName+' '+lastName))
		patientInfo = patient.json()['results'][0]
		print patientInfo
		patientAppointment = auth.getAppointmentsPerPatient(token, patientInfo['id'])
		if patientAppointment.status_code != 200:
			return HttpResponseNotFound("No appointments found today for Patient: {0}".format(firstName+' '+lastName))
		patientAppointmentData = patientAppointment.json()['results']
		if len(patientAppointmentData)==0:
			messages.error(request, "No appointment set for today")
			return redirect('/')
		currentIndex = utility.getLatestAppointment(patientAppointmentData)
		if currentIndex is None:
			messages.error(request, "No more appointment to Check In")
			return redirect('/')
		patientAppointmentData = patientAppointmentData[currentIndex]
		print "The true patient data is %s" %patientAppointmentData
		if patientAppointmentData['status'] == 'Arrived' or patientAppointmentData['status']=='Complete' or patientAppointmentData['status']=='In Session':
			messages.info(request, "Check in already done")
		elif patientAppointmentData['status'] == 'Cancelled':
			messages.error(request, "Appointmnet was cancelled")
		elif patientAppointmentData['status'] == 'Rescheduled':
			messages.error(request, "Appointment was rescheduled")
		else:
			context = {
			"patientId" : patientAppointmentData['patient'],
			"appointmentId" : patientAppointmentData['id'],
			}
			return render(request, "demographic.html", context)
		return redirect("home")
	else:
		return render(request, 'validatePatient.html', {})

def updateDemographic(request):
	if request.method=='POST':
		token = Token.objects.get(pk = request.session['user'])
		data = {
		"address" : request.POST['address'],
		"cell_phone" : request.POST['phone'],
		"zip_code" : request.POST['zipCode'],
		}
		patientId = request.POST['patientId']
		response = auth.updatePatientDemographicInfo(token, patientId, data)
		if response.status_code==400 or response.status_code==403 or response.status_code==409:
			messages.error(request, "Demographic data not updated.")
		else:
			messages.success(request, "Demographic data updated.")
		appointmentId = request.POST['appointmentId']
		status = "Arrived"
		update = auth.updatePatientAppointmentData(token, appointmentId, status)
		Appointment(appointmentId=appointmentId, checkIn = datetime.datetime.now()).save()
		if update.status_code==400 or update.status_code==403 or update.status_code==409:
			messages.error(request, "The status was not modified. Please try again")
		else:
			messages.success(request, "Check In successful")
		return redirect('home')

@login_required(login_url='login')
def stopTimer(request, id=None, st=None):
	obj = Appointment.objects.filter(appointmentId = id)
	print obj
	if len(obj)>0:
		obj[0].inSession = datetime.datetime.now()
		if st:
			obj[0].scheduled_time = st
		obj[0].save()
	status = "In Session"
	token = Token.objects.get(pk = request.session['user'])
	update = auth.updatePatientAppointmentData(token, id, status)
	if update.status_code==400 or update.status_code==403 or update.status_code==409:
		messages.error(request, "The status was not modified. Please try again")
	else:
		messages.success(request, "Check In successful")
	return redirect('home')

@login_required(login_url='login')
def complete(request, id=None):
	status = "Complete"
	token = Token.objects.get(pk = request.session['user'])
	update = auth.updatePatientAppointmentData(token, id, status)
	if update.status_code==400 or update.status_code==403 or update.status_code==409:
		messages.error(request, "The status was not modified. Please try again")
	else:
		messages.success(request, "Check In successful")
	return redirect('home')

@login_required(login_url='login')
def logoutUser(request):
	if 'user' in request.session:
		Token.objects.filter(pk=request.session['user']).delete()
		del request.session['user']
	logout(request)
	return redirect("/")