from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
    # ex: /app/
    url(r'^$', views.index, name='index'),
    # ex: /app/
    url(r'^view/$', views.view, name='view'),
    # ex: /app/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /app/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /app/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
