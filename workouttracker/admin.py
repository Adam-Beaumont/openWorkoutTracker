from django.contrib import admin

from workouttracker.models import Exercise, WorkoutExercise, Routine, RoutineExercise, Run

admin.site.register(Exercise)
admin.site.register(WorkoutExercise)
admin.site.register(Routine)
admin.site.register(RoutineExercise)
admin.site.register(Run)
# Register your models here.
