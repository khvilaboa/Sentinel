# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
		
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
	
    def __str__(self):
        return self.choice_text
		
class Camera(models.Model):
    url = models.CharField(max_length=200)
    num = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    longitude = models.IntegerField(default=0)
    latitude = models.IntegerField(default=0)

    def __str__(self):
        return self.description