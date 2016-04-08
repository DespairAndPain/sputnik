from django.db import models


class Comics(models.Model):
    comics_id = models.IntegerField(verbose_name='comics_id')
    title = models.CharField(max_length=250, verbose_name='title')
    series_id = models.IntegerField(verbose_name='series_id')
    creators_id = models.IntegerField(verbose_name='creators_id')
    heroes_id = models.IntegerField(verbose_name='heroes_id')


class ComicsList(models.Model):
    title_param = models.CharField(max_length=250, verbose_name='title_param')
    id_r = models.IntegerField(verbose_name='id_r')
    title_r = models.CharField(max_length=250, verbose_name='title_r')


class HeroEventsList(models.Model):
    name_param = models.CharField(max_length=250, verbose_name='name_param')
    name_r = models.IntegerField(verbose_name='name_r')
    events_r = models.CharField(max_length=2000, verbose_name='events_r')