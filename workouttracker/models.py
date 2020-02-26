from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import Sum
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ---------------------- Signal Recievers ---------------------------------

# Copies data from the "defaultdata" user into the new profile 
@receiver(post_save, sender=User)
def populate_default_exercises(sender,instance,created,**kwargs):
    if created:
        print(instance.id)
        for exercise in Exercise.objects.filter(user_id=4):
            newExercise = Exercise.create(
            getattr(exercise,'title'),
            getattr(exercise,'description'),
            getattr(exercise,'sets'),
            getattr(exercise,'reps'),
            instance
            )
            newExercise.save()

# -------------------For Management of Demo Accounts------------------------
class DemoManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isDemo = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_demo_manager(sender, instance, created, **kwargs):
    if created:
        DemoManager.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_demo_manager(sender, instance, **kwargs):
    instance.demomanager.save()

# -------------------------- Models ----------------------------------------

class RoutineQuerySet(models.QuerySet):
    def last_10(self):
        return self.order_by('name')[:10]

    def belongsTo(self, user):
        return self.filter(user=user)

    def routine(self, routine):
        return self.filter(routine=routine)

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

class WorkoutQuerySet(models.QuerySet):
    def dateDescending(self):
        return self.order_by('-date')

    def last_5(self):
        return self.order_by('date')[:5]

    def mostRecent(self):
        if self.count()==1:
            return self.get()
        else:
            if self.count()==0:
                return self.order_by('-date')[:1]
            else:
                return self.order_by('-date')[:1].get()

    def belongsTo(self, user):
        return self.filter(user=user)

class Workout(models.Model):
    date = models.DateField(default=date.today)
    description = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    objects = WorkoutQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'workouts'
        ordering = ['date']

    @classmethod
    def create(cls, description, user ):
        workout = cls(description=description, user=user)
        return workout

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse('workout_update', args=[self.id])

    def get_workoutExercises(self):
        return RoutineExercise.objects.filter(workout=self)


class ExerciseQuerySet(models.QuerySet):
    def last_10(self):
        return self.order_by('-date')[:10]
    
    def belongsTo(self, user):
        return self.filter(user=user)

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
        return reverse('exercise_update', args=[self.pk])

    @classmethod
    def create(cls, title, description, sets, reps, user ):
        exercise = cls(title=title, description=description,sets=sets,reps=reps, user=user)
        return exercise

class RunQuerySet(models.QuerySet):
    def dateDescending(self):
        return self.order_by('-date')

    def last_7(self):
        return self.order_by('date')[:7]
    
    def belongsTo(self, user):
        return self.filter(user=user)

    def mostRecent(self):
        if self.count()==1:
            return self.get()
        else:
            if self.count()==0:
                return self.order_by('-date')[:1]
            else:
                return self.order_by('-date')[:1].get()

    def totalDistance(self):
        return self.aggregate(Sum('distance'))['distance__sum']

class Run(models.Model):
    date = models.DateField('Date of Run',default=date.today)
    description = models.TextField(blank=True, null=True)
    distance = models.DecimalField('Distance Ran - In km',max_digits=6, decimal_places=2, blank=True, null=True)
    time = models.DecimalField('Time - In Minutes',max_digits=6, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    objects = RunQuerySet.as_manager()

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse('run_update', args=[self.pk])

class RoutineExerciseQuerySet(models.QuerySet):
    def routine(self, routine):
        return self.filter(routine=routine)
    
    def belongsTo(self, user):
        return self.filter(user=user)

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

    def belongsTo(self, user):
        return self.filter(user=user)

    def getForWorkout(self, workout):
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
    objects = WorkoutExerciseQuerySet.as_manager()
    
    @classmethod
    def create(cls, title, description, sets, reps, workout_id, user ):
        workoutExercise = cls(title=title, description=description,sets=sets,reps=reps,workout_id=workout_id, user=user)
        return workoutExercise

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return self.workout.get_absolute_url()

    def getworkout(self, workout_id):
        return self.filter(workout_id=workout_id)
