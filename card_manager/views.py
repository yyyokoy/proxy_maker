from django.shortcuts import render, redirect
from django.http import HttpResponse
from card_manager.models import Card

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from icrawler.builtin import GoogleImageCrawler

import glob
import sys
import base64
import json
import os
import subprocess
import shutil
import urllib.parse

def card_choice(request):

    def crawler(store_dir, keyword):
        try:
            files = os.listdir(store_dir)
            for file in files:
                try:
                    os.remove(store_dir + '/' + file)
                except OSError:
                    pass
        except OSError:
            pass

        crawler = GoogleImageCrawler(storage={"root_dir": store_dir})
        crawler.crawl(keyword=keyword, max_num=10, overwrite=True)

    if request.method == 'GET':
        card = ""
        files = []
        message = ''
        files_count = len(files)

        context = {
            'card_url': urllib.parse.quote(card),
            'files': files,
            'message': message,
            'files_count': files_count,
        }

        return render(request, 'card_manager/card.html', context)

    elif request.method == 'POST':
        card = request.POST.get('card', None)
        keyword = '遊戯王 ' + card
        store_dir = 'media/card/' + card
        # 指定した画像人物のクローリング
        crawler(store_dir, keyword)
        # 画像のリストを取得
        files = os.listdir(store_dir)
        files_count = len(files)
        # 人物を選択するメッセージを表示
        message = card + 'っぽい画像を選んでください'

        context = {
            'card_url': urllib.parse.quote(card),
            'card': card,
            'files': files,
            'message': message,
            'files_count': files_count,
        }


        return render(request, 'card_manager/card.html', context)

class ProxyView(TemplateView):
    template_name = "card_manager/proxy.html"
