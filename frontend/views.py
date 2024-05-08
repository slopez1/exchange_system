import base64
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views import View

from core.models import GlobalData, ExternalRequests, ABSSharedData
from core.tools.data_collectors import request_blockchain_data
from frontend.forms import *


# Create your views here.


class Man(View):
    template_name = 'data.html'

    def get(self, request):
        return render(request, self.template_name, context={'data': GlobalData.objects.all()})


class DataDetail(View):
    template_name = 'gb_detail.html'

    def _render(self, request, gb):
        data = None
        if gb.sync_status == GlobalData.ACCEPTED:
            data = request_blockchain_data(gb.identifier)
        return render(request, self.template_name, context={'gb': gb, 'data': data})

    def get(self, request, gb_pk):
        gb = get_object_or_404(GlobalData, pk=gb_pk)
        return self._render(request, gb)

    def post(self, request, gb_pk):
        gb = get_object_or_404(GlobalData, pk=gb_pk)
        gb.sync_status = GlobalData.PENDING
        gb.save()
        return self._render(request, gb)


class Requesters(View):
    template_name = 'external_request.html'

    def _get_decoded(self, d):
        if settings.BLOCKCHAIN_LAYER == 'Fabric':
            d.decoded = d.decode_requester().replace('x509::', '')
            d.decoded = d.decoded[0:d.decoded.find("::CN", 1)]
            d.decoded = d.decoded.replace(',', '\n')
        else:
            d.decoded = d.requester

    def _render(self, request):
        data = ExternalRequests.objects.all()
        for d in data:
            self._get_decoded(d)
        return render(request, self.template_name, context={'data': data})

    def get(self, request):
        return self._render(request)

    def post(self, request):
        external_request = ExternalRequests.objects.get(pk=request.POST['e_pk'])
        external_request.status = request.POST['status']
        external_request.synchronized = False
        external_request.save()
        return self._render(request)


class CreateData(View):
    template_name = 'create_data.html'

    def _render(self, request, correct=0, prev_forms=None):
        # Correct 0:Not sended - 1:Correct - 2: Error
        forms = [[ABSSharedDataForm.friendly_name, ABSSharedDataForm()], ]
        if CUSTOM_FORMS:
            forms = []
            for k in CUSTOM_FORMS:
                forms.append([k.friendly_name, k()])
        if prev_forms:
            print(prev_forms.errors)
            for t in forms:
                if t[0] == prev_forms.friendly_name:
                    t[1] = prev_forms
                    break
        return render(request, self.template_name, context={'forms': forms, 'correct': correct})

    def get(self, request):
        return self._render(request, 0, None)

    def post(self, request):
        model_type = request.POST['model_type']
        print(model_type)
        form = ABSSharedDataForm
        for k in CUSTOM_FORMS:
            if k.friendly_name == model_type:
                form = k
                break
        print(form)
        print(request.POST)
        form = form(request.POST)
        if form.is_valid():
            form.save()
            return self._render(request, 1)
        return self._render(request, 2, form)


class OwnData(View):
    template_name = 'own_data.html'

    def get(self, request):
        return render(request, self.template_name, context={'data': ABSSharedData.objects.all()})


class OwnDataDetail(View):
    template_name = 'own_data_detail.html'

    def _get_object_subclass(self, data_pk):
        data = get_object_or_404(ABSSharedData, pk=data_pk)
        sub_class = ABSSharedData
        for x in ABSSharedData.__subclasses__():
            instance = getattr(data, x.__name__.lower(), None)
            if instance:
                sub_class = x
                data = instance
                break
        return data, sub_class

    def _get_form(self, subclass):
        form = ABSSharedDataForm
        for f in CUSTOM_FORMS:
            if f.Meta.model == subclass:
                return f
        return form

    def get(self, request, data_pk):
        data, subclass = self._get_object_subclass(data_pk)
        form = self._get_form(subclass)
        return render(request, self.template_name, context={'data': data, 'form': form(instance=data), 'correct': 0})

    def post(self, request, data_pk):
        data, subclass = self._get_object_subclass(data_pk)
        form = self._get_form(subclass)
        p = request.POST.copy()
        p['identifier'] = data.identifier
        form = form(p, instance=data)
        correct = 2

        if form.is_valid():
            data = form.save(commit=False)
            data.synchronized = False
            data.save()
            correct = 1
        return render(request, self.template_name, context={'data': data, 'form': form, 'correct': correct})
