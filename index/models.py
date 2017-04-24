# -*- coding: utf-8 -*-
from django.db import models


class Department(models.Model):
    name = models.CharField(
        max_length=255,
    )
    url = models.CharField(
        max_length=1024,
    )

    gerb_url = models.CharField(
        max_length=1024, default=''
    )

    def __str__(self):
        return ' '.join([
            self.name
        ])


class AcademicSubject(models.Model):
    name = models.CharField(
        max_length=255,
    )

    url = models.CharField(
        max_length=1024,default='http://'
    )

    def __str__(self):
        return ' '.join([
            self.name,
        ])


class Direction(models.Model):
    name = models.CharField(
        max_length=255,
    )
    form_learn = models.CharField(
        max_length=255,
    )
    min_mark = models.CharField(
        max_length=255,default='0'
    )

    marks = models.CharField(max_length=1024, default=0)

    subjects_list = models.ManyToManyField(AcademicSubject)
    department_fk = models.ForeignKey(Department)

    def __str__(self):
        return ''.join([
            self.name,
        ])