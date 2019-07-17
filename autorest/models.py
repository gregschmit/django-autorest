# TODO: purely for dev testing, delete before pushing!


from django.db import models

class Thing(models.Model):
    name = models.CharField(max_length=255)
    is_cool = models.BooleanField(default=True)
    desc = models.TextField(blank=True)
