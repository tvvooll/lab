from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm


# Create your models here.
    
class Client(models.Model):
    client_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.client_name
    
class Task(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT)
    client = models.ForeignKey('Client', on_delete=models.PROTECT)
    comment = models.CharField(max_length=500)
    amount = models.IntegerField(default=10)
    
    
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=200)
    def __str__(self):
        return self.supplier_name
    
class SubmitTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['supplier','client','comment','amount']

    

    