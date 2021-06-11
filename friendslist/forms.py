from django import forms
from friendslist.models import Friend

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = (
            'name',
            'furigana',
            'nickname',
            'sex',
            'birthday',
            'birthplace',
            'hobby',
            'company',
        )