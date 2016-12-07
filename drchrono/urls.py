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
	url(r'^notActive', views.notActive, name='notActive'),
	url(r'^authorize', views.authorize, name='authorize'),
	url(r'^profile', views.profile, name='profile'),
	url(r'^(?P<id>\w+)/(?P<st>[0-9-:T]+)/stopTimer', views.stopTimer, name='stopTimer'),
	url(r'^(?P<id>\w+)/complete', views.complete, name='complete'),
	url(r'^patient', views.validatePatient, name='patient'),
	url(r'^demographic', views.updateDemographic, name='demographic'),
	url(r'^logout', views.logoutUser, name='logout'),
	# url(r'', include('social.apps.django_app.urls', namespace='social')),
]
