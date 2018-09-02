from django.shortcuts import render, redirect
from django.http import HttpResponse
from card_manager.models import Card, Deck

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

import glob
import sys
import base64
import json
import os
import subprocess
import shutil
from urllib import request as req
from urllib import error
from urllib import parse
import bs4

def card_choice(request):

    def crawler(card):

        keyword ='遊戯王' + str(card)

        urlKeyword = parse.quote(keyword)
        url = 'https://www.google.com/search?hl=jp&q=' + urlKeyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'

        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
        request = req.Request(url=url, headers=headers)
        page = req.urlopen(request)

        html = page.read().decode('utf-8')
        html = bs4.BeautifulSoup(html, "html.parser")
        elems = html.select('.rg_meta.notranslate')
        imageURLs = []
        counter = 0
        for ele in elems:
            ele = ele.contents[0].replace('"','').split(',')
            eledict = dict()
            for e in ele:
                num = e.find(':')
                eledict[e[0:num]] = e[num+1:]
            imageURL = eledict['ou']
            imageURLs.append(imageURL)

        return imageURLs[0:10]

    if request.method == 'GET':
        card = ""
        message = ''

        context = {
            'card_url': parse.quote(card),
            'message': message,
        }

        return render(request, 'card_manager/card.html', context)

    elif request.method == 'POST':
        card = request.POST.get('card', None)
        keyword = '遊戯王 ' + card
        card_url_list = crawler(card)
        message = card + 'っぽい画像を選んでください'

        context = {
            'card': card,
            'message': message,
            'card_url_list': card_url_list,
        }


        return render(request, 'card_manager/card.html', context)

def card_register(request):

    card = Card()

    if request.method == 'POST':
        selected_card = request.POST.get('selected_card', None)
        owner = request.user
        card.owner = owner
        card.card_source = selected_card.split(',')[0]
        card.name = selected_card.split(',')[1]
        card.save()
        print(owner)
        print(selected_card.split(',')[1])

    return redirect('card_manager:card_choice')

def card_pool(request):
    user = request.user
    cards = Card.objects.filter(owner=user).order_by('id')
    # decks = Deck.objects.filter(owner=user).order_by('id')
    context = {
        'cards': cards,
        # 'decks': decks,
    }
    return render(request, 'card_manager/card_pool.html', context)

class ProxyView(TemplateView):
    template_name = "card_manager/proxy.html"

def deck_list(request):
    """デッキの一覧"""
    user = request.user
    decks = Deck.objects.filter(owner=user).order_by('id')
    context = {
        'decks': decks,
    }
    return render(request, 'card_manager/deck_list.html', context)
