# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-17 17:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0014_serving'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Admin',
            new_name='TimetableManagement',
        ),
    ]