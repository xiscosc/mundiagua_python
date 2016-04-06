from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from client.models import Client, Address, Phone


class SearchClientBaseView(TemplateView):
    template_name = 'search_client.html'

    def post(self, request, *args, **kwargs):
        search = request.POST.getlist('search')[0]
        context = self.get_context_data()
        context['clients'] = Client.objects.filter(name__icontains=search)
        context['show_results'] = len(context['clients'])
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

    def get_context_data(self, **kwargs):
        context = super(SearchClientBaseView, self).get_context_data(**kwargs)
        context['show_results'] = -1
        return context


class CreateBaseView(CreateView):

    def get_form(self, form_class=None):
        form = super(CreateBaseView, self).get_form(form_class=form_class)
        form.fields['address'].queryset = Address.objects.filter(client=self.kwargs['id'])
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateBaseView, self).get_context_data(**kwargs)
        context['client'] = Client.objects.get(pk=self.kwargs['id'])
        context['phones'] = Phone.objects.filter(client=self.kwargs['id'])
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(CreateBaseView, self).form_valid(form)