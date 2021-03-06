from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from workouttracker.forms import ExerciseSelectForm, ExerciseForm, WorkoutFormSet
from workouttracker.models import Exercise, Routine, Workout, WorkoutExercise, RoutineExercise

import jsonpickle
from collections import namedtuple

class WorkoutIndex(LoginRequiredMixin, generic.ListView):
    template_name = 'workouttracker/workout_overview.html'
    context_object_name = 'workouts'
    model = Workout
    paginate_by = 50
    
    class workoutEntry:
        name=''
        exercises=[]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        if 'workoutexercise' in self.request.GET:
            queryset = queryset.filter(workoutexercise_id=self.request.GET['workoutexercise'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'workouts'
        workouts = context['workouts']
        workoutsList = []
        for workout in Workout.objects.belongsTo(self.request.user).dateDescending():
            entry = self.workoutEntry()
            entry.name = workout
            entry.exercises = WorkoutExercise.objects.filter(user=self.request.user).filter(workout_id=workout.id)
            workoutsList.append({"name": workout, "id": workout.id, "exercises": WorkoutExercise.objects.filter(user=self.request.user).filter(workout_id=workout.id)})

        context['workoutsList'] = workoutsList
        return context

class WorkoutExerciseCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Workout
    template_name = 'workouttracker/workout_form.html'
    formset_class = WorkoutFormSet
    fields = {'date','description'}

    def get_context_data(self, **kwargs):
        context = super(WorkoutExerciseCreate, self).get_context_data(**kwargs)
        context['exerciseSelect'] = Exercise.objects.belongsTo(self.request.user)
        context['exercises'] = jsonpickle.encode(Exercise.objects.belongsTo(self.request.user))
        context['formset'] = self.formset_class()
        context['menu'] = 'workouts'
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            workout = form.save(commit=False)
            formset = self.formset_class(self.request.POST, instance=workout)
            if formset.is_valid():
                workout.user = self.request.user
                workout.save()
                new_instances = formset.save(commit=False)
                for new_instance in new_instances:
                    new_instance.user = self.request.user
                    new_instance.save()
                return HttpResponseRedirect(reverse('workouts'))
        return self.render_to_response(self.get_context_data(form=form))

class WorkoutExerciseUpdate(UserPassesTestMixin, LoginRequiredMixin, generic.edit.UpdateView):
    model = Workout
    template_name = 'workouttracker/workout_form.html'
    formset_class = WorkoutFormSet
    fields = {'date','description'}
    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super(WorkoutExerciseUpdate, self).get_context_data(**kwargs)
        context['exerciseSelect'] = Exercise.objects.belongsTo(self.request.user)
        context['exercises'] = jsonpickle.encode(Exercise.objects.belongsTo(self.request.user))
        context['formset'] = self.formset_class(**self.get_form_kwargs())
        context['menu'] = 'workouts'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            workout = form.save(commit=False)
            formset = self.formset_class(self.request.POST, instance=workout)
            if formset.is_valid():
                workout.user = self.request.user
                workout.save()
                formset.save()
                return HttpResponseRedirect(reverse('workouts'))
        return self.render_to_response(self.get_context_data(form=form))
    
class WorkoutDelete(LoginRequiredMixin, generic.edit.DeleteView):
    model = Workout
    success_url = reverse_lazy('workouts')

    def get_context_data(self, **kwargs):
        context = super(WorkoutDelete, self).get_context_data(**kwargs)
        context['menu'] = 'workouts'
        return context

class WorkoutCreateFromRoutine(LoginRequiredMixin, generic.edit.CreateView):
    model = Workout
    fields = ['date','description']

    def post(self, request, *args, **kwargs):
        kwargs['pk']

        workout = Workout.create(getattr(Routine.objects.get(id=kwargs['pk']),'description'),self.request.user)
        workout.save()
        for RExercise in RoutineExercise.objects.filter(user=self.request.user).filter(routine_id=kwargs['pk']):
            workoutExercise = WorkoutExercise.create(
                getattr(RExercise,'title'),
                getattr(RExercise,'description'),
                getattr(RExercise,'sets'),
                getattr(RExercise,'reps'),
                getattr(workout,'id'),
                self.request.user
            )
            workoutExercise.save()
        return HttpResponseRedirect(reverse('workout_update', kwargs={'pk': getattr(workout,'id')}))
        # return self.render_to_response(self.get_context_data(form=form))
