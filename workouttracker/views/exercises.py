from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from workouttracker.forms import ExerciseForm
from workouttracker.models import Exercise
# from workouttracker.lib import last_day_of_month


class ExerciseDetail(LoginRequiredMixin, generic.DetailView):
    model = Exercise
    context_object_name = 'exercise'
    def get_context_data(self, **kwargs):
        context = super(ExerciseDetail, self).get_context_data(**kwargs)
        context['menu'] = 'exercises'
        return context


class ExerciseDelete(LoginRequiredMixin, generic.edit.DeleteView):
    model = Exercise
    success_url = reverse_lazy('exercises')

    def get_context_data(self, **kwargs):
        context = super(ExerciseDelete, self).get_context_data(**kwargs)
        context['menu'] = 'exercises'
        return context


class ExerciseIndex(LoginRequiredMixin, generic.ListView):
    template_name = 'workouttracker/exercises_overview.html'
    context_object_name = 'exercises'
    def get_queryset(self):
        return Exercise.objects.belongsTo(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'exercises'
        return context


class ExerciseCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Exercise
    template_name = 'workouttracker/exercise_form.html'
    form_class = ExerciseForm

    def get_context_data(self, **kwargs):
        context = super(ExerciseCreate, self).get_context_data(**kwargs)
        context['menu'] = 'exercises'
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = self.request.user
            exercise.save()
            return HttpResponseRedirect(reverse('exercises'))
        return self.render_to_response(self.get_context_data(form=form))


class ExerciseUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    model = Exercise
    template_name = 'workouttracker/exercise_form.html'
    form_class = ExerciseForm


    def get_context_data(self, **kwargs):
        context = super(ExerciseUpdate, self).get_context_data(**kwargs)
        context['form'] = self.form_class(**self.get_form_kwargs())
        context['menu'] = 'exercises'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            exercise = form.save(commit=False)
            form = self.form_class(self.request.POST, instance=exercise)
            if form.is_valid():
                exercise.save()
                form.save()
                return HttpResponseRedirect(reverse('exercises'))
        return self.render_to_response(self.get_context_data(form=form))
