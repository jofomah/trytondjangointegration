from django import forms
from trytonproteus.tryton_proteus import TrytonProteus


class AddPartyForm(forms.Form):
    tryton_proteus = TrytonProteus()
    party_name = forms.CharField(max_length=35, min_length=6, required=True)
    party_code = forms.CharField(max_length=35)
    party_lang = forms.ChoiceField(choices=tryton_proteus.get_lang_choices())

    address_name = forms.CharField()
    address_street = forms.CharField()
    address_zip = forms.CharField()
    address_city = forms.CharField()
    address_country = forms.ChoiceField(choices=tryton_proteus.get_country_choices())


