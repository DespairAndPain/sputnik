from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.db import connection
from .models import Comics, ComicsList, HeroEventsList
import urllib.request
import urllib.parse
import json
import hashlib
import re
global str


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


privat_key = 'f2aef3327f9d5859b700a4a52da3291dfd1b968c'
public_key = '31d015169ce2dc5756cb03569e2544cd'
ts = '1'


def comics_list(request):
    if request.method == 'GET':
        # берутся параметры из запроса
        page = request.GET.get('page')
        title = request.GET['title']
        di = {}
        if ComicsList.objects.all().filter(title_param=title):
            result = ComicsList.objects.all().filter(title_param=title)

            for i in result:
                di[''+i.id_r+''] = i.title_r
        else:
            # хэш функция ключей для аутентификации на сервере
            str = ts + privat_key + public_key
            m = hashlib.md5()

            m.update(str.encode('utf-8'))

            # параметры гет запроса у сервера
            params = urllib.parse.urlencode({'hash': m.hexdigest(), 'apikey': '31d015169ce2dc5756cb03569e2544cd', \
                                             'ts': '1', 'titleStartsWith': title, 'format': 'comic',
                                             })
            # получаем список комиксов сожержащих подстроку в заголовке
            url = "http://gateway.marvel.com:80/v1/public/comics?%s" % params
            print(url)
            if page is None:
                page = 1
                with urllib.request.urlopen(url) as f:
                    j = json.loads(f.read().decode('utf-8'))
                    count_items = len(j.get('data').get('results'))
                    if count_items > 10:
                        counter = 0
                        for i in j.get('data').get('results'):
                            if counter < 10:
                                di[i.get('id')] = i.get('title')

                    else:
                        for i in j.get('data').get('results'):
                            di[i.get('id')] = i.get('title')
                    # выставляются страницы
                    count_pages = round(count_items/10)
                    pages = count_pages
                    page = 1
            else:
                with urllib.request.urlopen(url) as f:
                    j = json.loads(f.read().decode('utf-8'))
                    count_pages = len(j.get('data').get('results'))

                    counter = 0
                    counts = int(page) * 10
                    previous = counts - 10

                    for i in j.get('data').get('results'):
                        if counter < counts and counter > previous:
                            di[i.get('id')] = i.get('title')
                        counter += 1
                    # выставляются страницы
                    count_pages = round(count_pages / 10)
                    pages = count_pages

            for i in di.items():
                comics_list_save = ComicsList(title_param=title, id_r=i[0], title_r=i[1])
                comics_list_save.save()
            response = {}
            response["page"] = page
            response["pages"] = pages
            response["result"] = di
    return JSONResponse(response)


def hero_events_list(request):
    if request.method == 'GET':

        page = request.GET.get('page')
        name = request.GET['name']
        di = {}

        if HeroEventsList.objects.all().filter(name_param=name):
            result = HeroEventsList.objects.all().filter(name_param=name)

            for i in result:
                di['' + i.name_r + ''] = i.events_r
        else:

            str = ts + privat_key + public_key
            m = hashlib.md5()
            m.update(str.encode('utf-8'))
            params = urllib.parse.urlencode({'hash': m.hexdigest(), 'apikey': '31d015169ce2dc5756cb03569e2544cd', \
                                             'ts': '1', 'nameStartsWith': name
                                             })

            # все события связанные с героем
            url = "http://gateway.marvel.com:80/v1/public/characters?%s" % params
            print(url)
            if page is None:
                with urllib.request.urlopen(url) as f:

                    j = json.loads(f.read().decode('utf-8'))
                    count_items = len(j.get('data').get('results'))

                    if count_items > 10:
                        counter = 0
                        for i in j.get('data').get('results'):
                            if counter < 10:
                                if len(i.get('events').get('items')) > 0:
                                    list = []
                                    for item in i.get('events').get('items'):
                                        list.append(item.get('name'))
                                    di[i.get('name')] = list
                                else:
                                    di[i.get('name')] = None
                            counter += 1
                    else:
                        for i in j.get('data').get('results'):
                            di[i.get('id')] = i.get('title')

                    count_pages = round(count_items / 10)
                    pages = count_pages
                    page = 1
            else:
                with urllib.request.urlopen(url) as f:
                    j = json.loads(f.read().decode('utf-8'))
                    count_items = len(j.get('data').get('results'))

                    counter = 0
                    counts = int(page) * 10
                    previous = counts - 10

                    for i in j.get('data').get('results'):
                        if counter < counts and counter > previous:
                            if len(i.get('events').get('items')) > 0:
                                list = []
                                for item in i.get('events').get('items'):
                                    list.append(item.get('name'))
                                di[i.get('name')] = list
                            else:
                                di[i.get('name')] = None
                        counter += 1

                    count_pages = round(count_items / 10)
                    pages = count_pages
            for i in di.items():
                events = ''
                for items in i[1]:
                    events = events + items
                comics_list_save = HeroEventsList(name_params=name, name_r=i[0], events_r=events)
                comics_list_save.save()

            response = {}
            response["page"] = page
            response["pages"] = pages
            response["result"] = di

    return JSONResponse(response)


def refresh_data(request):
    if request.method == 'GET':
        str = ts + privat_key + public_key
        m = hashlib.md5()
        m.update(str.encode('utf-8'))

        params = urllib.parse.urlencode({'hash': m.hexdigest(), 'apikey': '31d015169ce2dc5756cb03569e2544cd', \
                                         'ts': '1', 'format': 'comic'
                                         })

        url = "http://gateway.marvel.com:80/v1/public/comics?%s" % params

        with urllib.request.urlopen(url) as f:

            j = json.loads(f.read().decode('utf-8'))
            for i in j.get('data').get('results'):
                comics_id = i.get('id')
                if i.get('series').get('resourceURI') is not None:
                    series = re.findall('\w+', i.get('series').get('resourceURI'))[-1]

                    creators_items = i.get('creators').get('items')
                    creators_list = []
                    for item in creators_items:
                        if item.get('resourceURI') is not None:
                            creators_list.append(re.findall('\w+', item.get('resourceURI'))[-1])

                    heroes_items = i.get('characters').get('items')
                    heroes_list = []
                    for item in heroes_items:
                        if item.get('resourceURI') is not None:
                            heroes_list.append(re.findall('\w+', item.get('resourceURI'))[-1])

                    for creators_i in creators_items:
                        for heroes_i in heroes_items:
                            comics = Comics(comics_id=comics_id, series_id=series, heroes_id=heroes_i,\
                                            creators_id=creators_i)
                            comics.save()
        return JSONResponse({"status": 'updated'})


def similar_comics_data(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute('''SELECT a.title as title1, b.title as title2,
                                 a.series_id, a.heroes_id, a.creators_id, b.series_id, b.heroes_id, b.creators_id
                            FROM public.marvel_api_comics a
                            JOIN public.marvel_api_comics b
                              ON (a.comics_id!=b.comics_id AND a.creators=b.creators and a.series_id = b.series_id
                             and a.heroes_id = b.heroes_id) ''')
        rows = cursor.fetchall()

        response = {}
        counter = 0
        for i in rows:
            response[""+counter+""] = [i['title1'], i['title2']]
            counter += 1

        return JSONResponse(response)


def base(request):
    return render(request, 'base.html')