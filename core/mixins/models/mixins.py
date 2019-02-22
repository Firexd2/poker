from django.db import models


class NamedObjMixin(models.Model):
    name = models.TextField("Name", blank=True, null=True)

    class Meta:
        abstract = True


class OnOffMixin(models.Model):
    is_enabled = models.BooleanField("Enabled", default=True, blank=True)

    class Meta:
        abstract = True

