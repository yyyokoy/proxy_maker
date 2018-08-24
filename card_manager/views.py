from django.shortcuts import render, redirect
from django.http import HttpResponse
from card_manager.models import Card

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

    def clrawler(card):

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

        return imageURLs[0:11]

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
        # 指定した画像人物のクローリング
        card_url_list = clrawler(card)
        # 画像のリストを取得
        # 人物を選択するメッセージを表示
        message = card + 'っぽい画像を選んでください'

        context = {
            'card': card,
            'message': message,
            'card_url_list': card_url_list,
        }


        return render(request, 'card_manager/card.html', context)

class ProxyView(TemplateView):
    template_name = "card_manager/proxy.html"
