# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from party.forms import AddPartyForm
from trytonproteus.tryton_proteus import TrytonProteus
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.shortcuts import redirect

PARTY_HOME_TEMPLATE = 'party/show_all_parties.html'
PARTY_DETAIL_TEMPLATE = 'party/party_detail.html'
ADD_PARTY_TEMPLATE = 'party/add_party.html'
ADD_PARTY_SUCCESSFUL_URL = '/party/add/successful/'

class PartyView(ListView):
    def get(self, request, *args, **kwargs):
        tryton_proteus = TrytonProteus()
        return render(request, PARTY_HOME_TEMPLATE, {'party_list': tryton_proteus.get_all_parties(),},)


class PartyDetailView(DetailView):
    def get(self, request, * args, ** kwargs):
        tryton_proteus = TrytonProteus()
        return render(request, PARTY_DETAIL_TEMPLATE, {'party': tryton_proteus.find_party_by_id(kwargs['party_id']),},)

class PartyRemoveView(DeleteView):
    def get(self, request, *args, **kwargs):
        tryton_proteus = TrytonProteus()
        tryton_proteus.delete_party_by_id(kwargs['party_id'])
        return render(request, PARTY_HOME_TEMPLATE, {'party_list': tryton_proteus.get_all_parties()},)



class PartyAddView(CreateView):
    def get(self, request, *args, **kwargs):
        return render(request, ADD_PARTY_TEMPLATE, {'form': AddPartyForm()},)

    def post(self, request, *args, **kwargs):
        add_party_form = AddPartyForm(request.POST)
        if add_party_form.is_valid():
            try:
                tryton_proteus = TrytonProteus()
                add_party_form = add_party_form.cleaned_data

                Party = tryton_proteus.get_model('party.party')
                Address = tryton_proteus.get_model('party.address')
                Country = tryton_proteus.get_model('country.country');
                Lang = tryton_proteus.get_model('ir.lang')

                party = Party()
                party.name = add_party_form['party_name']
                party.code = add_party_form['party_code']
                lang_code = add_party_form['party_lang']
                party.lang = Lang.find([('code', '=', lang_code)])[0]

                address_country = Country.find([('code', '=', add_party_form['address_country'])])[0]
                address = Address(name=add_party_form['address_name'],
                                        street=add_party_form['address_street'],
                                        zip=add_party_form['address_zip'],
                                        city=add_party_form['address_city'],
                                        country=address_country)
                party.addresses.append(address)
                party.save()

                return HttpResponseRedirect(ADD_PARTY_SUCCESSFUL_URL)
            except BaseException as e:
                return render(request, ADD_PARTY_TEMPLATE, {'form': AddPartyForm(), 'exception_msg': e.message},)
        return render(request, ADD_PARTY_TEMPLATE, {'form': add_party_form},)
