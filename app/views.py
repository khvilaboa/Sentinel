# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Camera

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
        'page_num':1,
        'page_title': "Inicio"
    }
    return render(request, 'app/index.html', context)

def view(request):
    context = {
        'page_num':2,
        'page_title':"Ver info chula"
    }
    return render(request, 'app/view.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'app/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'app/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('app:results', args=(question.id,)))
	
def cameras_json(request):
    """data = Play.objects.all() \
        .extra(select={'month': connections[Play.objects.db].ops.date_trunc_sql('month', 'date')}) \
        .values('month') \
        .annotate(count_items=Count('id'))"""
    data = {c.description: [c.longitude, c.latitude,c.num, c.url] for c in Camera.objects.all()}
    #data = [{"type": "Cameras", "objects": {}}]
    return JsonResponse(data, safe=False)

def map(request):
    return render(request, 'app/mapa.html')
