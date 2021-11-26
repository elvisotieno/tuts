from django.db import models

# Create your models here.
class Diseases(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=30)
    status = models.CharField(max_length=30, blank=True, null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.CharField(max_length=20,blank=True, null=True)
    causes = models.CharField(max_length=80)
    treatment = models.TextField(max_length=255)

    def __str__(self):
        return self.name