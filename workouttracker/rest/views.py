from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from workouttracker.models import Workout, WorkoutExercise, Exercise, Routine, RoutineExercise, Run
from workouttracker.rest import serializers
from workouttracker.rest.serializers import (WorkoutSerializer,
                                           WorkoutExerciseSerializer,
                                           ExerciseSerializer, RoutineSerializer, 
                                           RoutineExerciseSerializer, RunSerializer)

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
