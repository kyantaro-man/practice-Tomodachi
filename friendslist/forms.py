from django import forms
from friendslist.models import Friend
from django.contrib.auth import get_user_model

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

class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user