from django.contrib import admin
from card_manager.models import Card, Deck, UserDecks


admin.site.register(Card)
admin.site.register(Deck)
admin.site.register(UserDecks)
