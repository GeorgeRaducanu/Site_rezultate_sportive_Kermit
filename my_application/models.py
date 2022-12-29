from django.db import models


class Echipe(models.Model):
    nume = models.CharField(max_length=50, primary_key=True)
    tara = models.CharField(max_length=40)
    antrenor = models.CharField(max_length=50)
    premii = models.PositiveIntegerField(default=0)


class Meci(models.Model):
    echipa1 = models.CharField(max_length=50)
    echipa2 = models.CharField(max_length=50)
    goluri1 = models.PositiveIntegerField(default=0)
    goluri2 = models.PositiveIntegerField(default=0)
    data = models.DateField()
    loc = models.CharField(max_length=100)
