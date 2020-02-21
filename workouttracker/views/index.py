from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views import generic
from django.core.serializers import serialize
import jsonpickle
import json

from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token as AuthToken
from workouttracker.lib import last_day_of_month
from workouttracker.models import Workout, Run


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'workouttracker/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'home'
        context['workoutsTotal'] = Workout.objects.belongsTo(self.request.user).count()
        context['lastWorkout'] = Workout.objects.belongsTo(self.request.user).mostRecent()
        context['runTotal'] = Run.objects.belongsTo(self.request.user).totalDistance()
        context['runChartData'] = serialize('json',Run.objects.belongsTo(self.request.user).only('date'))
        context['lastRun'] = Run.objects.belongsTo(self.request.user).mostRecent()
        return context
