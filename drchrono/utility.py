#To perform various miscellaneous tasks
from datetime import datetime

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
