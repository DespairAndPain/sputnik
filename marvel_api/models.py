from django.db import models


class Series(models.Model):
    series_id = models.IntegerField(verbose_name='series_id')


class Creators(models.Model):
    creators_id = models.IntegerField(verbose_name='creators_id')


class Heroes(models.Model):
    heroes_id = models.IntegerField(verbose_name='heroes_id')


class Comics(models.Model):
    comics_id = models.IntegerField(verbose_name='comics_id')
    s_id = models.IntegerField(verbose_name='s_id')
    c_id = models.IntegerField(verbose_name='c_id')
    h_id = models.IntegerField(verbose_name='h_id')

