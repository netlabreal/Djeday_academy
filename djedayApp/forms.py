from django import forms


class FormCandidate(forms.Form):
    name = forms.CharField(required=True, max_length=100)
    age = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    planet = forms.IntegerField(required=True)


