from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from workouttracker.forms import RunForm
from workouttracker.models import Run
# from workouttracker.lib import last_day_of_month


class RunDetailView(LoginRequiredMixin, generic.DetailView):
    model = Run
    context_object_name = 'run'
    def get_context_data(self, **kwargs):
        context = super(RunDetailView, self).get_context_data(**kwargs)
        context['menu'] = 'runs'
        return context


class RunDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Run
    success_url = reverse_lazy('runs')

    def get_context_data(self, **kwargs):
        context = super(RunDeleteView, self).get_context_data(**kwargs)
        context['menu'] = 'runs'
        return context


class RunIndex(LoginRequiredMixin, generic.ListView):
    template_name = 'workouttracker/runs_overview.html'
    context_object_name = 'runs'
    def get_queryset(self):
        return Run.objects.belongsTo(self.request.user).dateDescending()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'runs'
        today = date.today()
        context['submenu'] = 'all'
        return context


class RunCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Run
    template_name = 'workouttracker/run_form.html'
    form_class = RunForm

    def get_context_data(self, **kwargs):
        context = super(RunCreate, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            run = form.save(commit=False)
            run.user = self.request.user
            run.save()
            return HttpResponseRedirect(reverse('runs'))
        return self.render_to_response(self.get_context_data(form=form))


class RunUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    model = Run
    template_name = 'workouttracker/run_form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(RunCreate, self).get_context_data(**kwargs)
        context['formset'] = self.formset_class(**self.get_form_kwargs())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            run = form.save(commit=False)
            formset = self.formset_class(self.request.POST, instance=run)
            if formset.is_valid():
                run.save()
                formset.save()
                return HttpResponseRedirect(reverse('runs',
                                                        args=[run.id]))
        return self.render_to_response(self.get_context_data(form=form))
