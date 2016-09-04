#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Occurence(models.Model):
    timestamp = models.DateTimeField(null=False)
    source = models.CharField(max_length=25, null=False)

    class Meta:
        unique_together = (('timestamp', 'source'),)
        get_latest_by = 'occurence'


class RateManager(models.Manager):

    def increase_or_create(self, item, occurence):
        itemtype = ContentType.objects.get_for_model(item)
        rate, created = Rate.objects.get_or_create(
            occurence=occurence, content_type=itemtype, object_id=item.id)
        rate.weight += 1
        rate.save()
        return rate


class Rate(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    weight = models.IntegerField(default=0, null=False)
    occurence = models.ForeignKey(to=Occurence, null=False)
    objects = RateManager()

    class Meta:
        unique_together = (('content_type', 'object_id', 'occurence'),)


class Word(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    rate = GenericRelation(Rate)


class Link(models.Model):
    address = models.URLField(unique=True, null=False)
    title = models.TextField(null=False)
    words = models.ManyToManyField(to=Word)
    rate = GenericRelation(Rate)

    class Meta:
        unique_together = (('address', 'title'),)
