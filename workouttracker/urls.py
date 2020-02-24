from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework import routers
from rest_framework.authtoken import views as drf_views
from workouttracker.rest import views as rest_views
from workouttracker.views import index as general_views
from workouttracker.views import routines as routine_views
from workouttracker.views import exercises as exercise_views
from workouttracker.views import workouts as workout_views
from workouttracker.views import runs as run_views


router = routers.DefaultRouter()
router.register(r'routines', rest_views.RoutineViewSet)
router.register(r'exercises', rest_views.ExerciseViewSet)
router.register(r'runs', rest_views.RunViewSet)
router.register(r'workouts', rest_views.WorkoutViewSet)

urlpatterns = [
    path('', general_views.IndexView.as_view(), name='index'),

    path('accounts/', include('allauth.urls')),

    path('routines/', routine_views.RoutineIndex.as_view(), name='routines'),
    path('workouts/', workout_views.WorkoutIndex.as_view(), name='workouts'),
    path('routines/<int:pk>/edit/',
         routine_views.RoutineExerciseUpdate.as_view(), name='routine_update'),
    path('routines/<int:pk>/asworkout/',
         workout_views.WorkoutCreateFromRoutine.as_view(), name='routine_as_workout'),
     path('routines/<int:pk>/delete/',
         routine_views.RoutineDelete.as_view(), name='routine_delete'),
    path('workouts/<int:pk>/edit/',
         workout_views.WorkoutExerciseUpdate.as_view(), name='workout_update'),
    path('workouts/<int:pk>/delete/',
         workout_views.WorkoutDelete.as_view(), name='workout_delete'),
    path('routine/create/',
         routine_views.RoutineExerciseCreate.as_view(), name='routine_create'),
    path('workout/create/',
         workout_views.WorkoutExerciseCreate.as_view(), name='workout_create'),
    path('exercise/create/',
         exercise_views.ExerciseCreate.as_view(), name='exercise_create'),
    path('exercise/<int:pk>/edit/',
         exercise_views.ExerciseUpdate.as_view(), name='exercise_update'),
    path('exercise/<int:pk>/delete/',
         exercise_views.ExerciseDelete.as_view(), name='exercise_delete'),
    path('exercises/',
         exercise_views.ExerciseIndex.as_view(), name='exercises'),
    path('runs/<int:pk>/delete/',
         run_views.RunDelete.as_view(), name='run_delete'),
    path('runs/<int:pk>/edit/',
         run_views.RunUpdate.as_view(), name='run_update'),
    path('runs/create/',
         run_views.RunCreate.as_view(), name='run_create'),
    path('runs/',
         run_views.RunIndex.as_view(), name='runs'),
    path('manifest.json', TemplateView.as_view(template_name='workouttracker/manifest.json'),
         name='manifest'),

    path('rest/', include(router.urls)),

]
