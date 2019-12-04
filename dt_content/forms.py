from django import forms

from .models import *


class MenuForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        Menu.objects.filter(parent=None),
        disabled=True,
        required=False,
        initial=None,
        widget=forms.HiddenInput(),
    )

    class Meta:
        fields = ["title", "url_slug", "disabled", "redirect_to", "parent"]
        model = Menu


class SubmenuForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        Menu.objects.filter(parent=None), disabled=True, widget=forms.HiddenInput()
    )

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
