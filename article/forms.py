from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","content","image"]
        widgets = {
            "title": forms.TextInput(attrs = {"placeholder": "Dikkat çekici bir başlık"}),
        }
