from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
    # ex: /app/
    url(r'^$', views.index, name='index'),
    # ex: /app/cameras_json
    url(r'^cameras_json/$', views.cameras_json, name='cameras_json'),
	# ex: /app/intens_json
    url(r'^intens_json/$', views.intens_json, name='intens_json'),
    # ex: /app/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /app/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /app/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    # ex: /app/map
    url(r'^map/$', views.view_map, name='view_map'),
]
