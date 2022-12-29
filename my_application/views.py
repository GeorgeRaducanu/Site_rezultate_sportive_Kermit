from django.http import HttpResponse
from django.template import loader

import os
import random
from .models import Echipe, Meci
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin


# Uncomment if you want to delete all the matches
# for x in Meci.objects.all():
#     x.delete()

# Uncomment if you want to delete all the teams
# for x in Echipe.objects.all():
#     x.delete()

# One-time addition of teams to the database
# echipe = [  Echipe('FCSB','Romania','Mihai Pintilii',1),
#             Echipe('Dinamo','Romania','Mircea Rednic',0),
#             Echipe('CFR Cluj','Romania','Dan Petrescu',1),
#             Echipe('Barcelona','Spain','Xavi',4),
#             Echipe('Real Madrid','Spain','Zinedine Zidane',3),
#             Echipe('Paris Saint Germain','France','Christophe Galtier',2),
#             Echipe('Bayern','Germany','Hans-Dieter Flick',3),
#             Echipe('Arsenal','UK','Mikel Arteta',1),
#             Echipe('Chelsea','UK','Graham Potter',2),
#             Echipe('Dinamo Russia','Russia','Slavisa Jokanovic',1),
#             Echipe('Manchester','UK','Nate Jensen',2),
#             Echipe('Juventus','Italy','Massimiliano Allegri',1),
#             Echipe('Liverpool','UK','Kenny Dalglish',0),
#             Echipe('Dynamo Kiev','Ukraine','Mircea Lucescu',1),
#             Echipe('Borussia Dortmund','Germany','Edin Terzic',0),
#             Echipe('Tottenham','UK','Antonio Conte',1),
#             Echipe('AC Milan','Italy','Stefano Pioli',2),
#             Echipe('Ajax','Netherlands','Erik ten Hag',0),
#             Echipe('Inter Milan','Italy','Simone Inzaghi',0),
#             Echipe('Porto','Portugal','Sergio Conceicao',1),
#             Echipe('Nottingham Forest','UK','Steve Cooper',2),
#             Echipe('Glasgow Celtic','UK','Ange Postecoglou',1),
#             Echipe('Santos','Brazil','Fernando',0),
#             Echipe('Torino','Italy','Ivan Juric',1),
#             Echipe('Sepsi','Romania','Cristiano Bergodi',1),
#             Echipe('Poli','Romania','Bogdan Andone',0),
# ]
# Echipe.objects.bulk_create(echipe)

@csrf_protect
def my_application(request):
    if request.method == 'POST':
        search_term = request.POST.get('cautare', '')
        try:
            echipa = Echipe.objects.get(nume=search_term)
            meciuri = Meci.objects.filter(echipa1=search_term) | Meci.objects.filter(echipa2=search_term)

            context = {
                'echipa': echipa,
                'meciuri': meciuri,
            }
            return render(request, 'prelucrare.html', context)
        except Echipe.DoesNotExist:
            context = {
                'error': 'No team found'
            }
            return render(request, 'prelucrare.html', context)
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


@xframe_options_sameorigin
def foo_1(request):
    context = {}
    template = loader.get_template('soccer_info.html')
    return HttpResponse(template.render(context, request))


@xframe_options_sameorigin
def foo_2(request):
    context = {}
    template = loader.get_template('emblem_check.html')
    return HttpResponse(template.render(context, request))


@xframe_options_sameorigin
def foo_3(request):
    context = {}
    template = loader.get_template('art_gallery.html')
    return HttpResponse(template.render(context, request))


def comentarii(request):
    context = {}
    template = loader.get_template('comentarii.html')
    return HttpResponse(template.render(context, request))


def prelucrare(request):
    context = {}
    template = loader.get_template('prelucrare.html')
    return HttpResponse(template.render(context, request))


@xframe_options_sameorigin
@csrf_protect
def inscrieri(request):
    if request.method == 'POST':
        echipe = Echipe.objects.create(
            nume=request.POST['nume'],
            tara=request.POST['tara'],
            antrenor=request.POST['antrenor'],
        )

        if echipe:
            message = "It worked fine, thanks :) See you at the next competition!"
        else:
            message = "Maybe try again, babe :("

        # Check if a file was uploaded
        if 'fisier' in request.FILES:
            uploaded_file = request.FILES['fisier']
            file_path = os.path.join('uploads', uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.read())
            message += "\n What a nice emblem! :O"
        else:
            message += "\n Your emblem couldn't be uploaded :("

        template = loader.get_template('echipa_created.html')
        context = {'message': message}
        return HttpResponse(template.render(context, request))

    return render(request, "inscrieri.html")


def search_team(nume_echipa):
    echipe = Echipe.objects.all()
    for echipa in echipe:
        if echipa.nume == nume_echipa:
            return echipa
    return None


def add_wins(goluri1, goluri2, echipa1, echipa2):
    if goluri1 > goluri2:
        winner = search_team(echipa1)
    else:
        winner = search_team(echipa2)
    winner.premii += 1
    winner.save()


@xframe_options_sameorigin
@csrf_protect
def meciuri(request):
    if request.method == 'POST':
        echipa1 = request.POST['e']
        echipa2 = Echipe.objects.exclude(nume=echipa1).order_by('?').first()
        goluri1 = random.randint(0, 16)
        goluri2 = random.randint(0, 16)
        data = request.POST['data']
        loc = request.POST['loc']
        meci = Meci.objects.create(echipa1=echipa1, echipa2=echipa2.nume, goluri1=goluri1, goluri2=goluri2, data=data,
                                   loc=loc)
        if meci:
            aux = "It worked fine, thanks! :) \nYou'll be playing against... "
            message = aux + echipa2.nume
            aux = message
            message = aux + " at the desired place on the chosen day!\nSee you at the match! :)"
            add_wins(goluri1, goluri2, echipa1, echipa2)
        else:
            message = "Maybe try again later! :("

        template = loader.get_template('meci_created.html')
        context = {'message': message}
        return HttpResponse(template.render(context, request))
    else:
        return render(request, 'meciuri.html')
