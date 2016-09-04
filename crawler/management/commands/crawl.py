#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from crawler.crawler_manager import CrawlerManager


class Command(BaseCommand):
    help = "My crawl command."

    def handle(self, *args, **options):
        cm = CrawlerManager()
        cm.crawl()
        self.stdout.write("Doing All The Things!")
