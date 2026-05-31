from django.db import models

from openedx_catalog.models_api import CatalogCourse

from ..models import PathwayItemCriteria


#################### This is specific to Courses  ####################
class CoursePathwayItemCriteria(PathwayItemCriteria):
    """
    This is a hypothetical PathwayItemCriteria type that can be satisifed by
    a catalog course (as opposed to a specific run).

    The problem with this is that it's not just about passing the course,
    individual criteria might be much more specific, like > 90% on the course.

    Have to migrate course pre-reqs into this?

    Always have to have an override option.
    """
    catalog_course = models.ForeignKey(CatalogCourse)