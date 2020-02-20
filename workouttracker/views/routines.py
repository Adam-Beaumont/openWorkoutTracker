from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from workouttracker.forms import ExerciseSelectForm, ExerciseForm, RoutineFormSet
from workouttracker.models import Exercise, Routine, RoutineExercise

import jsonpickle
from collections import namedtuple

class RoutineIndex(LoginRequiredMixin, generic.ListView):
    template_name = 'workouttracker/routine_overview.html'
    context_object_name = 'routines'
    model = Routine
    paginate_by = 50
    
    class routineEntry:
        name=''
        exercises=[]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if 'routineexercise' in self.request.GET:
            queryset = queryset.filter(routineexercise_id=self.request.GET['routineexercise'])

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'routines'
        context['submenu'] = 'all'
        routines = context['routines']
        routinesList = []
        for routine in routines:
            entry = self.routineEntry()
            entry.name = routine
            entry.exercises = RoutineExercise.objects.belongsTo(self.request.user).filter(routine_id=routine.id)
            routinesList.append({"name": routine, "id": routine.id, "exercises": RoutineExercise.objects.filter(routine_id=routine.id)})

        context['routinesList'] = routinesList
    
        return context

class RoutineExerciseCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Routine
    template_name = 'workouttracker/routine_split_form.html'
    formset_class = RoutineFormSet
    fields = {'name','description'}

    def get_context_data(self, **kwargs):
        context = super(RoutineExerciseCreate, self).get_context_data(**kwargs)
        context['exerciseSelect'] = Exercise.objects.belongsTo(self.request.user)
        context['exercises'] = jsonpickle.encode(Exercise.objects.belongsTo(self.request.user))
        context['formset'] = self.formset_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            routine = form.save(commit=False)
            formset = self.formset_class(self.request.POST, instance=routine)
            if formset.is_valid():
                routine.user = self.request.user
                routine.save()
                new_instances = formset.save(commit=False)
                for new_instance in new_instances:
                    new_instance.user = self.request.user
                    new_instance.save()
                return HttpResponseRedirect(reverse('routines'))
        return self.render_to_response(self.get_context_data(form=form))

class RoutineExerciseUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    model = Routine
    template_name = 'workouttracker/routine_split_form.html'
    formset_class = RoutineFormSet
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(RoutineExerciseUpdate, self).get_context_data(**kwargs)
        context['exerciseSelect'] = Exercise.objects.belongsTo(self.request.user)
        context['exercises'] = jsonpickle.encode(Exercise.objects.belongsTo(self.request.user))
        context['formset'] = self.formset_class(**self.get_form_kwargs())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())

        if form.is_valid():
            routine = form.save(commit=False)
            formset = self.formset_class(self.request.POST, instance=routine)
            if formset.is_valid():
                routine.user = self.request.user
                routine.save()
                formset.save()
                return HttpResponseRedirect(reverse('routines'))
        return self.render_to_response(self.get_context_data(form=form))