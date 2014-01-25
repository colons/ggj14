from django import forms

from ggj14.apps.chat.script import parse_script


class SetCustomScriptForm(forms.Form):
    script = forms.CharField(widget=forms.Textarea, validators=[parse_script])
