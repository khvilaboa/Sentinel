# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Camera

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Camera)