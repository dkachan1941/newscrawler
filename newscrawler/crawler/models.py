# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

class News(models.Model):
	title = models.CharField(max_length=250, unique=True)
	text = models.TextField()
	date = models.DateTimeField()
	category = models.CharField(max_length=250)

	def __str__(self):
		return '%s' % (self.title)

	class Meta:
		verbose_name = "Новость"
		verbose_name_plural = "Новости"

	def __unicode__(self):
		return u"%s" % (self.title)