from __future__ import annotations

from django.conf import settings
from django.db import models

from openedx_django_lib.fields import code_field
from ..publishing.models import PublishableEntity, PublishableEntityVersion
from ..media.models import Media


class PathwayType(models.Model):
    """
    Labeled PathwayTypes may be set at a system or maybe even org level.
    Examples: Tier, Group, Pathway.

    Questions:

    1. What other metadata is associated with a PathwayType?
    2. How do we properly serialize PathwayTypes across instances, if they can
       be set on a per-instance basis?
    3. If PathwayTypes could be set at an Org level, do we have to worry about
       different orgs having semantically different types with the same name?
    """
    type_code = code_field(unicode=False, unique=True)


class Pathway(PublishableEntity):
    """
    The top level Pathway model.

    A Pathway represents some type of student journey, whether that's some set
    of courses or more granular content. It is very open ended, and potentially
    very long-lived, e.g. a degree program. This means that we have to be
    prepared for the possibility that a Pathway will change significantly over
    time, and that people will care very much about the state that a Pathway was
    in at the time that some Student completed it.
    """
    pathway_type = models.ForeignKey(PathwayType, on_delete=models.RESTRICT)
    pathway_code = code_field()


class PathwayVersion(PublishableEntityVersion):
    """
    How do we determine if a Pathway is complete?
    Can we encode rules in CEL? https://cel.dev/
    Example:
      // each item is a StudentPathwayItem
      all(items, item.complete && item.grade > 0.8)
    It probably makes sense to make more than one type of
    PathwayCompletionCriteria, but I hope CEL can do a lot of the work.
    """
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE)
    completion_criteria = models.ForeignKey(Media, on_delete=models.RESTRICT)



class PathwayItemType(models.Model):
    type_code = code_field()


class PathwayItem(PublishableEntity):
    """
    A single step in a pathway.
    Examples: "Intro CS Course", "HW Assignment 20", etc.
    """
    pathway_item_type = models.ForeignKey(
        PathwayItemType, on_delete=models.CASCADE
    )
    pathway_item_code = code_field()


class PathwayItemVersion(PublishableEntityVersion):
    pass


class PathwayVersionPathwayItem(models.Model):
    pathway_version = models.ForeignKey(PathwayVersion, on_delete=models.CASCADE)
    pathway_item = models.ForeignKey(PathwayItem, on_delete=models.RESTRICT)



class PathwayItemCriteria(models.Model):
    """
    This represents a potential way to fulfill a PathwayItem.
    It is abstract.
    It is not strictly necessary. A CoursePathwayItemAttempt might point
    to a CoursePathwayItemCriteria, but
    """
    item = models.ForeignKey(PathwayItem)
    required_completion_level = models.FloatField(null=True)
    required_grade = models.FloatField(null=True)

