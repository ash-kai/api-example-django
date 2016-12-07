#To perform various miscellaneous tasks
from datetime import datetime
from .models import Appointment

def validatePatient(parameter):
	pass
	# to Validate a patient for doctor's appointment

def getTodaysAppointments(parameter):
	pass
	# To get current days appointments

def getLatestAppointment(patientAppointments):
	index = None
	currentTimestamp = datetime.now()
	print currentTimestamp
	for i in range(len(patientAppointments)):
		if patientAppointments[i]['status']=='Arrived' or patientAppointments[i]['status']=='Completed' or patientAppointments[i]['status']=='Cancelled' or patientAppointments[i]['status']=='Rescheduled':
			pass
		else:
			time = str(patientAppointments[i]['scheduled_time'])
			time = time.replace('T',' ')
			timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
			if (timestamp-currentTimestamp).total_seconds() < 0:
				index = i
			else:
				break
	if index is None:
		for i in range(len(patientAppointments)):
			if patientAppointments[i]['status']=='Arrived' or patientAppointments[i]['status']=='Completed' or patientAppointments[i]['status']=='Cancelled' or patientAppointments[i]['status']=='Rescheduled':
				pass
			else:
				time = str(patientAppointments[i]['scheduled_time'])
				time = time.replace('T',' ')
				timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
				if (timestamp-currentTimestamp).total_seconds() > 0:
					index = i
				else:
					break
	return index

def getAverageTime():
	average = []
	cnt = 0 
	appointments = Appointment.objects.filter(scheduled_time__startswith = datetime.now().date())
	for appointment in appointments:
		if appointment.checkIn is not None and appointment.inSession is not None:
			cnt+=1
			if (appointment.checkIn-appointment.scheduled_time).total_seconds()<0:
				startTime = appointment.scheduled_time
			else:
				startTime = appointment.checkIn
			average.append((appointment.inSession-startTime).total_seconds())
	if cnt==0:
		return 0
	return sum(average)/cnt