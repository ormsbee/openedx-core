from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


from openedx_django_lib.fields import code_field, case_insensitive_char_field
from ..publishing.models import PublishableEntity, PublishableEntityVersion
from ..media.models import Media
from ....openedx_catalog.models_api import CatalogCourse, CatalogPathway


class Pathway(PublishableEntity):
    pathway_code = code_field()


class CatalogPathwayLookup(models.Model):
    """
    Mapping from CatalogPathways to content Pathways.

    CatalogPathways and Pathways may be managed by different people.

    CatalogPathways may be 1:M with Pathway content.
    """
    catalog_pathway = models.ForeignKey(CatalogPathway, on_delete=models.CASCADE, unique=True)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE)


class PathwayVersion(PublishableEntityVersion):
    """

    """
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Media, on_delete=models.RESTRICT)


class PathwayStepType(models.Model):
    type_code = code_field()


class PathwayStep(PublishableEntity):
    """
    A single step in a pathway.
    Examples: "Intro CS Course", "HW Assignment 20", etc.
    """
    step_type = models.ForeignKey(PathwayStepType, on_delete=models.CASCADE)
    step_code = code_field()


class CatalogCourseStep(PathwayStep):
    catalog_course = models.ForeignKey(CatalogCourse, on_delete=models.RESTRICT)


class StepVersion(PublishableEntityVersion):
    criteria = models.ForeignKey(Media, on_delete=models.RESTRICT)


class PathwayVersionStep(models.Model):
    pathway_version = models.ForeignKey(PathwayVersion, on_delete=models.CASCADE)
    step = models.ForeignKey(PathwayStep, on_delete=models.RESTRICT)
    order_num = models.PositiveIntegerField(null=True)
