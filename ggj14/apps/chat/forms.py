from django import forms


class SetCustomScriptForm(forms.Form):
    script = forms.CharField(widget=forms.Textarea)
