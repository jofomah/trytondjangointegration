
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from trytonproteus.tryton_proteus import TrytonProteus


class ModuleView(ListView):
    def get(self, request, *args, **kwargs):
        tryton_proteus = TrytonProteus()
        return render(request, 'modulemanager/modules.html', {'module_list': tryton_proteus.get_modules(),})


class InstallModuleView(UpdateView):
    def get(self, request, *args, **kwargs):
        tryton_proteus = TrytonProteus()
        tryton_proteus.install_module(kwargs['module_id'])
        return HttpResponseRedirect('/module/')
