# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string

import imobiliaria


class Permalinkable(models.Model):
    slug = models.SlugField(default=get_random_string)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('%s:%s_detail' % (self._meta.app_label,
                                         self._meta.model_name),
                       args=(self.slug,))


class SingletonSiteManager(models.Manager):
    """
        Returns only a single preferences object per site.
    """
    def get_queryset(self):
        """
            Return the first preferences object for the current site.
            If preferences do not exist create it.
        """
        queryset = super(SingletonSiteManager, self).get_queryset()
        return queryset

    def get(self, *args, **kws):
        """ Always returns the current site record """
        if not self.model.singleton.all():
            new_object = self.model.singleton.create()
            return new_object
        return self.get_queryset().get()


class Preferences(models.Model):
    """ Abstract model for Site Preferences. see the below doc. """

    objects = models.Manager()
    singleton = SingletonSiteManager()

    class Meta:
        abstract = True


@receiver(models.signals.class_prepared)
def preferences_class_prepared(sender, *args, **kwargs):
    """
    Adds preferences dynamically to imobiliaria.preferences,
    thus enabling easy access from code like this:

    # Getting a value preference
    >>> from imobiliaria import preferences
    >>> field_one = preferences.MyCustomPreferences.field_one

    # Saving a new value
    >>> my_custom_pref = MyCustomPreferences.singleton.get()
    >>> my_custom_pref.field_one = 'updated'
    >>> my_custom_pref.save()

    For a given model preferences:
    class MyCustomPreferences(Preferences):
        field_one = models.CharField(...)
        field_two = models.CharField(...)
    """

    cls = sender

    if issubclass(cls, Preferences):
        cls.add_to_class('singleton', SingletonSiteManager())
        setattr(imobiliaria.Preferences, cls._meta.object_name,
                property(lambda x: cls.singleton.get()))
