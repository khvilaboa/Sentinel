# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Camera

import xml.etree.cElementTree as ET
import urllib2, csv, pyproj, os

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

def intens_json(request):
    cr = csv.reader(open(os.path.join("data", "intens_points.csv"), "rb"), delimiter=str(";"))
    coords = {row[0]:(row[4], row[5]) for row in cr}

    e = ET.ElementTree(file=urllib2.urlopen('http://informo.munimadrid.es/informo/tmadrid/pm.xml'))
    #e = xml.etree.ElementTree.parse('pm.xml').getroot()
    pms = [l for l in e.findall("pm")]

    cont = 0
    res = {}

    kl = ["codigo", "descripcion", "intensidad", "ocupacion", "carga", "accesoAsociado", "nivelServicio", "subarea", "intensidadSat"]
    
    for pm in pms:
        pmc = pm.getchildren()
        tags = map(lambda x: x.tag, pmc)
        texts = map(lambda x: x.text, pmc)
        
        if any([t not in tags for t in kl]):
            continue
            
        for ind, t in enumerate(texts):
            if t is None:
                if ind == 1:
                    texts[ind] = ""
                else:
                    texts[ind] = -1
                    
        if texts[1] == "":
            continue
            
        cont += 1
        #print texts
        
        code = texts[tags.index("codigo")]
		
        if code not in coords:
            continue

        utm_x, utm_y = map(lambda x: float(x.replace(",", ".")), list(coords[code]))
        huso = 30
        elipsoide1 = "intl"
        srcProj = pyproj.Proj(proj="utm", zone=huso, ellps=elipsoide1, units="m")
        dstProj = pyproj.Proj(proj='longlat', ellps='WGS84', datum='WGS84')
        long,lat = pyproj.transform(srcProj, dstProj, utm_x, utm_y)
        res[code] = [texts[tags.index(ke)] if ind == 1 else int(texts[tags.index(ke)]) for ind,ke in enumerate(kl)] + [long, lat]
        #res[texts[tags.index("codigo")]] = [texts[tags.index(ke)] if ind == 1 else int(texts[tags.index(ke)]) for ind,ke in enumerate(kl)]
    
    return JsonResponse(res, safe=False)
    #return HttpResponse(pms[0].getchildren()[0].text)
    
def view_map(request):
    return render(request, 'app/mapa.html')


    