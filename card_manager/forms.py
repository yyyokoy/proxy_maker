from django.forms import ModelForm
from card_manager.models import UserDecks


class UserDecksForm(ModelForm):
    """デッキのフォーム"""
    class Meta:
        model = UserDecks
        fields = ('name', )
