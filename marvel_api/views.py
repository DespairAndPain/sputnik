from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import urllib.request
import urllib.parse
import json
import hashlib
global str

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def ComicsList(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        print(page)

        title = request.GET['title']
        privat_key = 'f2aef3327f9d5859b700a4a52da3291dfd1b968c'
        public_key = '31d015169ce2dc5756cb03569e2544cd'
        ts = '1'

        str = ts + privat_key + public_key
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        params = urllib.parse.urlencode({'hash': m.hexdigest(), 'apikey': '31d015169ce2dc5756cb03569e2544cd', \
                                         'ts': '1', 'titleStartsWith': title, 'format': 'comic',
                                         })
        url = "http://gateway.marvel.com:80/v1/public/comics?%s" % params
        print(url)
        di = {}
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
                count_pages = round(count_items/10)
                di['pages'] = count_pages
                di['page'] = 1
        else:
            with urllib.request.urlopen(url) as f:
                j = json.loads(f.read().decode('utf-8'))
                count_pages = len(j.get('data').get('results'))

                counter = 0
                page = int(page)*10
                previous = page - 10

                for i in j.get('data').get('results'):
                    if counter < page and counter > previous:
                        di[i.get('id')] = i.get('title')
                    counter += 1

                di['pages'] = count_pages
                di['page'] = 1

    return JSONResponse(di)


        # if len(i.get('events').get('items'))>0:
        #    list = []
        #    for item in i.get('events').get('items'):
        #        list.append(item.get('name'))
        #    di[i.get('name')] = list
        # else:
        #    di[i.get('name')] = None