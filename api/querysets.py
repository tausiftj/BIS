from django.db import models
from django.utils.timezone import localtime


class BaseModelQuerySet(models.QuerySet):

    def update(self, **kwargs):
        kwargs.update(updated=localtime())
        return super().update(**kwargs)
    update.alters_data = True