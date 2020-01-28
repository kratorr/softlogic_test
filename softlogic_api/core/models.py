from django.db import models
#from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.
class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100) #TODO not null
    last_name = models.CharField(max_length=100) #TODO not null
    vector = models.CharField(blank=True, null=False, max_length=1500)