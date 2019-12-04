from django import forms

from .models import *


class SubmenuCreateForm(forms.ModelForm):
    parent = forms.ModelChoiceField(Menu.objects.filter(parent=None), disabled=True)

    class Meta:
        fields = ["title", "url_slug", "disabled", "redirect_to", "parent"]
        model = Menu


class RichTextBlockCreateForm(forms.ModelForm):
    section = forms.ModelChoiceField(
        ContentSection.objects.get_queryset(), disabled=True
    )

    class Meta:
        fields = ["content", "section"]
        model = RichTextBlock
