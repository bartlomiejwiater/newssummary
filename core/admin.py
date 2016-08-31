#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Word, Link, Occurence, Rate


admin.register(Word)
admin.register(Link)
admin.register(Occurence)
admin.register(Rate)
