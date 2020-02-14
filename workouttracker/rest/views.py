from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from workouttracker.models import Workout, WorkoutExercise, Exercise, Routine, RoutineExercise
from workouttracker.rest import serializers
from workouttracker.rest.serializers import (WorkoutSerializer,
                                           WorkoutExerciseSerializer,
                                           ExerciseSerializer, RoutineSerializer, RoutineExerciseSerializer)

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
