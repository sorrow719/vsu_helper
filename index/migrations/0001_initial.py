# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 17:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(default='http://', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=1024)),
                ('gerb_url', models.CharField(default='', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('form_learn', models.CharField(max_length=255)),
                ('min_mark', models.CharField(default='0', max_length=255)),
                ('marks', models.CharField(default=0, max_length=1024)),
                ('department_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Department')),
                ('subjects_list', models.ManyToManyField(to='index.AcademicSubject')),
            ],
        ),
    ]
