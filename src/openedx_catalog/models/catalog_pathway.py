from django.db import models

from organizations.models import Organization


class CatalogPathway(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.RESTRICT)

