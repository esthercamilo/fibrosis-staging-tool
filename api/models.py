from django.db import models
from django.contrib.auth.models import User


class Institution(models.Model):
    """
    Instituição que organizou a questão, por exemplo: USP, UNESP.
    """
    DoesNotExist = None
    id = models.AutoField(primary_key=True)
    sigla = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=200, null=True)

