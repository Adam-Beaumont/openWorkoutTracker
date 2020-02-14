from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from workouttracker.forms import ExerciseSelectForm, ExerciseForm, WorkoutFormSet
from workouttracker.models import Exercise, Workout, WorkoutExercise

import jsonpickle
from collections import namedtuple

# class WorkoutIndex(LoginRequiredMixin, generic.ListView):
class WorkoutIndex(generic.ListView):
    template_name = 'workouttracker/workout_overview.html'
    context_object_name = 'workouts'
    model = Workout
    paginate_by = 50
    
    class workoutEntry:
        name=''
        exercises=[]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if 'workoutexercise' in self.request.GET:
            queryset = queryset.filter(workoutexercise_id=self.request.GET['workoutexercise'])

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'workouts'
        context['submenu'] = 'all'
        workouts = context['workouts']
        workoutsList = []
        for workout in workouts:
            entry = self.workoutEntry()
            entry.name = workout
            entry.exercises = WorkoutExercise.objects.filter(workout_id=workout.id)
            workoutsList.append({"name": workout, "id": workout.id, "exercises": WorkoutExercise.objects.filter(workout_id=workout.id)})

        context['workoutsList'] = workoutsList
        return context

# class WorkoutExerciseCreate(LoginRequiredMixin, generic.edit.CreateView):
class WorkoutExerciseCreate(generic.edit.CreateView):
    model = Workout
    template_name = 'workouttracker/workout_split_form.html'
    formset_class = WorkoutFormSet
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(WorkoutExerciseCreate, self).get_context_data(**kwargs)
        context['exerciseSelect'] = ExerciseSelectForm
        context['exercises'] = jsonpickle.encode(Exercise.objects.all())
        context['formset'] = self.formset_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            workout = form.save(commit=False)
            formset = self.formset_class(self.request.POST, instance=workout)
            if formset.is_valid():
                workout.save()
                formset.save()
                return HttpResponseRedirect(reverse('workouts'))
        return self.render_to_response(self.get_context_data(form=form))

# class WorkoutExerciseUpdate(LoginRequiredMixin, generic.edit.UpdateView):
class WorkoutExerciseUpdate(generic.edit.UpdateView):
    model = Workout
    template_name = 'workouttracker/workout_split_form.html'
    formset_class = WorkoutFormSet
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(WorkoutExerciseUpdate, self).get_context_data(**kwargs)
        context['exerciseSelect'] = ExerciseSelectForm
        context['exercises'] = jsonpickle.encode(Exercise.objects.all())
        context['formset'] = self.formset_class(**self.get_form_kwargs())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            workout = form.save(commit=False)
            formset = self.formset_class(self.request.POST, instance=workout)
            if formset.is_valid():
                workout.save()
                formset.save()
                return HttpResponseRedirect(reverse('workouts'))
        return self.render_to_response(self.get_context_data(form=form))
    