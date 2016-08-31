#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management import BaseCommand


class Command(BaseCommand):
    # Show this when the user types help
    help = "My test command"

    # A command must define handle()
    def handle(self, *args, **options):
        self.stdout.write("Doing All The Things!")
