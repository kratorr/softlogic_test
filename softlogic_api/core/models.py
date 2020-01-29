from django.db import models
import uuid


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    vector = models.TextField(blank=True, null=True)