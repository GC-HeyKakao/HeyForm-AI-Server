from djongo import models


class SurveyTitle(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)