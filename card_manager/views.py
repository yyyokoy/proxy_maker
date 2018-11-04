from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from card_manager.models import Card, Deck, UserDecks
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from card_manager.forms import UserDecksForm

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


@login_required
def card_choice(request):

    def crawler(card):

        keyword ='遊戯王' + str(card)

        urlKeyword = parse.quote(keyword)
        url = 'https://www.google.com/search?hl=jp&q={}&btnG=Google+Search&tbs=0&safe=off&tbm=isch'.format(urlKeyword)

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
        keyword = '遊戯王 {}'.format(card)
        card_url_list = crawler(card)
        message = card + 'っぽい画像を選んでください'

        context = {
            'card': card,
            'message': message,
            'card_url_list': card_url_list,
        }


        return render(request, 'card_manager/card.html', context)

@login_required
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

@login_required
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

def card_del(request, card_id):
    """カードの削除"""
#     return HttpResponse('書籍の削除')
    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return redirect('card_manager:card_pool')

@login_required
def deck_list(request):
    """デッキの一覧"""
    user = request.user
    decks = UserDecks.objects.filter(owner=user).order_by('id')
    context = {
        'decks': decks,
    }
    return render(request, 'card_manager/deck_list.html', context)

def deck_edit(request, deck_id=None):
    # TODO: リファクタリング
    """デッキの編集"""
    user_id = request.user.id
    owner = User.objects.get(id=user_id)

    if deck_id:   # book_id が指定されている (修正時)
        deck = get_object_or_404(UserDecks, pk=deck_id)
    else:         # book_id が指定されていない (追加時)
        deck = UserDecks()

    if request.method == 'POST':
        form = UserDecksForm(request.POST, instance=deck)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            deck = form.save(commit=False)
            deck.owner = owner
            deck.save()
            return redirect('card_manager:deck_list')
    else:    # GET の時
        form = UserDecksForm(instance=deck)  # book インスタンスからフォームを作成

    return render(request, 'card_manager/deck_edit.html', dict(form=form, deck_id=deck_id))
