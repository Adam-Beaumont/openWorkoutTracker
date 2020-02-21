from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from workouttracker import models

class RoutineForm(forms.ModelForm):
    class Meta:
        model = models.Routine
        fields = ['name','description']

    def save(self, commit=True):
        routine = super().save(commit)
        routine.save()
        models.RoutineExercise.objects.create(routine=routine)
        return routine

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = models.Workout
        fields = ['description']

    def save(self, commit=True):
        workout = super().save(commit)
        workout.save()
        models.WorkoutExercise.objects.create(workout=workout)
        return workout

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = models.Exercise
        fields = ('title','dateAdded', 'description', 'sets', 'reps')

    def save(self, commit=True):
        exercise = super().save(commit)
        return exercise

class RunForm(forms.ModelForm):
    class Meta:
        model = models.Run
        fields = ('date','description', 'distance', 'time')

    def save(self, commit=True):
        run = super().save(commit)
        return run

class ExerciseSelectForm(forms.ModelForm):
    class Meta:
        model = models.Exercise
        fields = ['title', 'description','reps','sets']
        widgets = {'title' : forms.HiddenInput(), 'description' : forms.HiddenInput(),
        'reps' : forms.HiddenInput(), 'sets' : forms.HiddenInput()}
    existing_exercises = forms.ModelChoiceField(queryset=models.Exercise.objects) 

class RoutineExerciseForm(forms.ModelForm):
    class Meta:
        model = models.RoutineExercise
        fields = ['title', 'description','reps','sets']

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = models.WorkoutExercise
        fields = ['title', 'description','reps','sets']

    
RoutineFormSet = forms.models.inlineformset_factory(
    models.Routine, models.RoutineExercise, form=RoutineExerciseForm, extra=1
    )

WorkoutFormSet = forms.models.inlineformset_factory(
    models.Workout, models.WorkoutExercise, form=WorkoutExerciseForm, extra=1
    )
        