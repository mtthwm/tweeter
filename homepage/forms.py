from django import forms
from django.forms import ModelForm
from homepage.models import Tweet, User, Search

class NewTweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]
        labels = {
            "content": "",
        }        

    def __init__(self, *args, **kwargs):
        super(NewTweetForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'p-5'
        self.fields['content'].widget.attrs['placeholder'] = "What's Happening?"

class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ["text"]
        labels = {
            "text": "",
        }
