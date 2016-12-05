from django.conf.urls import include, url
# from django.views.generic import TemplateView

import views


urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^$', views.index, name='home'),
	url(r'^authorize', views.authorize, name='authorize'),
	url(r'^profile', views.profile, name='profile'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
