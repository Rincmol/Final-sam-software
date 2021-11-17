#from django.contrib.auth.models import DemoPCash
from .models import DemoPCash
from rest_framework import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = DemoPCash
        fields = ['account', 'ledger_name','date', ]