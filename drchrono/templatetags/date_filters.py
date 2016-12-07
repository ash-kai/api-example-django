from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter('date_format')
def get_due_date_string(value):
	value = value.replace('T',' ')
	return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

@register.filter('time_format')
def get_due_date_string(value):
	h, m = map(int, divmod(value, 60))
	
	return "%d hour %d minutes" % (h, m)

@register.filter('waiting_time')
def get_waiting_time(value):
	print value
	# value = value.replace('T',' ')
	# startTime = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
	# secconds = (datetime.now()-startTime).total_seconds()
	# if secconds<0:
	# 	return "0 minutes"
	# else:
	# 	m,s = map(int, divmod(secconds,60))
	# 	if m<60:
	# 		return "%s minutes"%m
	# 	h,m = map(int, divmod(m, 60))
	# 	return "%s hour %s minutes"%(h,m)