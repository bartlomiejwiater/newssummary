#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType


class Word(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)


class Link(models.Model):
    address = models.URLField(unique=True, null=False)
    title = models.TextField(null=False)
    words = models.ManyToManyField(to=Word)

    class Meta:
        unique_together = (('address', 'title'),)

class Occurence(models.Model):
    timestamp = models.DateTimeField(null=False)
    source = models.CharField(max_length=25, null=False)

    class Meta:
        unique_together = (('timestamp', 'source'),)
        get_latest_by = 'occurence'


class Rate(models.Model):
    item = models.ForeignKey(ContentType, null=False)
    weight = models.IntegerField(default=0, null=False)
    occurence = models.ForeignKey(to=Occurence, null=False)

    class Meta:
        unique_together = (('item', 'occurence'),)
