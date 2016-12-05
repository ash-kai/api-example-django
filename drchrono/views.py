from django.shortcuts import render, redirect
# Create your views here.
from . import authenticate

def index(request):
    if 'doctor' in request.session:
        d = utility.get_doctor(request.session['doctor'])
        appointments = utility.getTodaysAppointments(d)
        context = {
                "appointments": appointments
        }
        return render(req, "appointmentDashboard.html", context)

    context = {
        "client_id": authenticate.client_id,
    }
    return render(request, "index.html", context)
