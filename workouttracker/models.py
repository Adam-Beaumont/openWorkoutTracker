from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.db import models
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class RoutineQuerySet(models.QuerySet):
    def last_10(self):
        return self.order_by('name')[:10]

# -------------------------- Adam's Stuff ----------------------------------------

class Routine(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    objects = RoutineQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'routines'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('routine_update', args=[self.id])

    def get_routineExercises(self):
        return RoutineExercise.objects.filter(routine=self)

class Workout(models.Model):
    date = models.DateField(default=date.today)
    description = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    objects = RoutineQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'workouts'
        ordering = ['date']

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse('workout_update', args=[self.id])

    def get_workoutExercises(self):
        return RoutineExercise.objects.filter(workout=self)

class ExerciseQuerySet(models.QuerySet):
    def last_10(self):
        return self.order_by('-date')[:10]

class Exercise(models.Model):
    title = models.CharField(max_length=64)
    dateAdded = models.DateField(default=date.today)
    description = models.TextField(blank=True, null=True)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    objects = ExerciseQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('exercise_create', args=[self.pk])

class RoutineExerciseQuerySet(models.QuerySet):
    def routine(self, routine):
        return self.filter(routine=routine)

class RoutineExercise(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    routine = models.ForeignKey(Routine, models.CASCADE, related_name='routineexercises',
                                    blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    objects = RoutineExerciseQuerySet.as_manager()

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return self.routine.get_absolute_url()

    def getroutine(self, routine_id):
        return self.filter(routine_id=routine_id)

class WorkoutExerciseQuerySet(models.QuerySet):
    def workout(self, workout):
        return self.filter(workout=workout)

class WorkoutExercise(models.Model): 
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    workout = models.ForeignKey(Workout, models.CASCADE, related_name='workoutexercises',
                                    blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    objects = RoutineExerciseQuerySet.as_manager()

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return self.workout.get_absolute_url()

    def getworkout(self, workout_id):
        return self.filter(workout_id=workout_id)
