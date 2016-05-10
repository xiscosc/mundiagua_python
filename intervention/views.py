# -*- coding: utf-8 -*-
from async_messages import message_user, constants
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, View

from core.models import User
from core.views import SearchClientBaseView, CreateBaseView
from intervention.models import Intervention, Zone, InterventionLog, InterventionStatus, InterventionModification


class HomeView(TemplateView):
    template_name = 'home.html'


class SearchClientView(SearchClientBaseView):

    def get_context_data(self, **kwargs):
        context = super(SearchClientView, self).get_context_data(**kwargs)
        context['title'] = "Nueva Avería"
        context['new_url'] = "intervention-intervention-new"
        context['btn_text'] = "Crear avería"
        context['btn_class'] = "btn-danger"
        return context


class CreateInterventionView(CreateBaseView):
    model = Intervention
    fields = ['address', 'description', 'zone']
    template_name = "new_intervention.html"

    def get_success_url(self):
        return reverse_lazy('intervention-intervention', kwargs={'pk': self.object.pk})


class InterventionView(DetailView):
    model = Intervention
    context_object_name = "intervention"
    template_name = "detail_intervention.html"

    def get_context_data(self, **kwargs):
        context = super(InterventionView, self).get_context_data(**kwargs)
        context['zones'] = Zone.objects.all()
        context['users'] = User.objects.all()
        context['status'] = InterventionStatus.objects.all()
        return context


class UpdateInterventionView(View):

    def post(self, request, *args, **kwargs):
        params = request.POST.copy()
        intervention = Intervention.objects.get(pk=kwargs['pk'])
        intervention._old_status_id = intervention.status_id
        intervention._old_assigned_id = intervention.assigned_id
        intervention_save = True

        try:
            intervention.status_id = int(params.getlist('intervention_status')[0])
        except IndexError:
            pass

        try:
            intervention.zone_id = int(params.getlist('intervention_zone')[0])
        except IndexError:
            pass

        try:
            modification_text = params.getlist('intervention_modification')[0]
            modification = InterventionModification(intervention=intervention, note=modification_text,
                                                    created_by=request.user)
            modification.save()
            intervention_save = False
        except IndexError:
            pass

        try:
            user_to_send = User.objects.get(pk=int(params.getlist('user_to_send')[0]))
            intervention.send_to_user(user_to_send)
            intervention_save = False
        except IndexError:
            pass

        if intervention_save:
            intervention._current_user = request.user
            intervention.save()

        message_user(request.user, "Modificación realizada correctamente", constants.SUCCESS)
        return HttpResponseRedirect(reverse_lazy('intervention-intervention', kwargs={'pk': intervention.pk}))
