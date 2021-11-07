from django.db import models

from api.querysets import BaseModelQuerySet


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db)

    def update(self, payload, **kwargs):
        return self.get_queryset().update(**kwargs)