from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views import generic

from rest_framework.authtoken.models import Token as AuthToken
from workouttracker.lib import last_day_of_month


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'workouttracker/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'home'
        return context
