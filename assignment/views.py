from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import re
import json

def scrap(request,info):
    print(info)
    output = {}
    URL = "https://en.wikipedia.org/wiki/" + info
    
    r = requests.get(URL)
    # print(r.content)
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    # print(soup.prettify())
    table = soup.find('img',attrs={'class' : 'thumbborder', 'decoding' : 'async'})
    
    # print(table)

    output['flag_link'] = table['src']
#######################################################################
    table = soup.find('div',attrs={'id' : 'mw-content-text'})

    trTags = table.find('td',attrs={'class' : 'infobox-data'}).find('a')
    # trTags = table.findAll('a')
    # trTags = table.findChildren()
    # abc = trTags.f
    
    output['Capital'] = trTags.get_text()
########################################################################
    # ,attrs={'class' : 'mergedbottomrow'}
    field2 = table.find('tbody').find('tr',attrs={'class' : 'mergedbottomrow'}).find_all('a')
    cities = []
    i=0
    for f in field2:
    # if(i<2):
        # print(i)
        try:
            cities.append(f['title'])
        except:
            print("Title Not Present")
        
        
        # i = i+1

    # print(cities)
    output['Largest_city']=cities
    #####################################################################
    field3 = table.find('tbody').find('tr',attrs={'class' : 'mergedtoprow'}).find_all('a')
    official_languages = []
    for f in field3:
    # if(i<2):
        # print(i)
        try:
            official_languages.append(f['title'])
        except:
            print("Official Language Not Present")
    
    output['official_languages'] = official_languages
    #####################################################################
    field4 = table.find('tbody').findAll('tr',attrs={'class' : 'mergedrow'})
    # field4 = BeautifulSoup(field4, 'html5lib')
    # a = field4.find('td',attrs={'class' : 'infobox-data'}).find('span')
    # for f in field4:
    field4Str = str(field4)
    data = (" ".join(re.findall(r'"(\d\d+)"', field4Str)))
    data = data.split(' ')
    output['area_total'] = data[0]
    output['population'] = data[1]
    output['GDP_nominal'] = data[2]
    #####################################################################
    # print(population)
    # print(type(field4Str))
    # print(data)
    output = json.dumps(output)
    # print(output)

    return HttpResponse(output)