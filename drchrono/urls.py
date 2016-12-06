from django.conf.urls import include, url
# from django.views.generic import TemplateView
import views
from django.contrib import admin


urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='index'),
	url(r'^login', views.loginUser, name='login'),
	url(r'^home', views.home, name='home'),
	url(r'^dashboard', views.dashboard, name='dashboard'),
	url(r'^authorize', views.authorize, name='authorize'),
	url(r'^profile', views.profile, name='profile'),
	url(r'^(?P<id>\w+)/stopTimer', views.stopTimer, name='stopTimer'),
	url(r'^patient', views.validatePatient, name='patient'),
	url(r'^demographic', views.updateDemographic, name='demographic'),
	url(r'^logout', views.logoutUser, name='logout'),
	url(r'', include('social.apps.django_app.urls', namespace='social')),
]
