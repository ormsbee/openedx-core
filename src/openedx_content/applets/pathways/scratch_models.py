from django.conf import settings
from django.db import models

from openedx_django_lib.fields import (
    case_insensitive_char_field,
    code_field,
    manual_date_time_field,
)
from ..publishing.models import PublishableEntity, PublishableEntityVersion
from ..media.models import Media


## Below this is all student functionality

class StudentPathwayProgress(models.Model):
    """
    TODO: This needs some status indicator of their completion, but also
    potentially things like DEMONSTRATED_MASTERY, or more granular
    categories of competency/mastery...
    Or is that separate? Is the thing that decides "what is your progress and
    when are you done with the Pathway" actually different from "what does your
    performance in the Pathway equate to in terms of your credential?"
    """
    pathway = models.ForeignKey(Pathway, on_delete=models.RESTRICT)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

class StudentPathwayItem(models.Model):
    """
    The status for this Student on a particular Item in a Learning Pathway.
    For example, if a PathwayItem represents, "Must pass one of the
    following course runs with a grade of at least 80%", then there might be a
    StudentPathwayItem that represents, "Student A passed Course Run C
    with a grade of 84%".
    A student may require multiple attempts to achieve a PathwayItem's
    requirements. We capture those attempts in StudentPathwayItemAttempt. Note
    that StudentPathwayItemAttempt -> StudentPathwayItem is NOT for the purposes
    of aggregation. If we want to model something like, "The student must pass
    these four Course Runs with grades of > 80%," that is a Pathway with four
    PathwayItems that can each be satisfied by one of those Course Runs.
    For a given StudentPathwayItem, we should be able to point to exactly one
    StudentPathwayItemAttempt that represents the "active" one. So if someone
    failed a previous Course Run and is trying again, the active_attempt will
    shift to that new CoursePathwayItemAttempt.
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    item = models.ForeignKey(PathwayItem, on_delete=models.RESTRICT)
    status = models.ForeignKey(StudentPathwayItemStatus, on_delete=models.PROTECT)
    active_attempt = models.ForeignKey(
        'PathwayItemAttempt',
        null=True,
    )


class PathwayItemAttempt(models.Model):
    """
    This follows the status of a given attempt to fulfill a pathway item.
    For instance, this could represent a student's grade on a particular Course
    Run as it changes over time, or it could represent the grade for a
    particular subsection in a CBE context.
    This does not give a full history of progress within a given attempt. So
    there will only be one of these rows for a given student's progress in a
    given course run. If we had to create a new row for every change, the size
    of this table would explode, and that kind of data collection is better
    handled by eventing/analytics.
    """
    student_pathway_item = models.ForeignKey(
        StudentPathwayItem,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    grade = models.FloatField(default=0.0)
    completion_level = models.FloatField(default=0.0)

    created = manual_date_time_field()
    updated = manual_date_time_field()




class CoursePathwayItemAttempt(PathwayItemAttempt):
    """
    Docstring for CoursePathwayItemAttempt

    Can one attempt satisfying multiple criteria? Could be one course that fits multiple criteria.
    What if the criteria changes?
    """
    criteria = models.ForeignKey(CoursePathwayItemCriteria, on_delete=models.RESTRICT)
    course_run = key_field()  # This should eventually be an fkey to CourseRun (or learning context?)


#################### Admin/Manual Override  ####################

class ManualOverridePathwayItemAttempt(PathwayItemAttempt):
    overridden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='+',
    )

#################### Competencies  ####################

class SubsectionPathwayItemCriteria(PathwayItemCriteria):
    # Should probably be a fkey to a Usage model
    usage_key = models.CharField()

class SubsectionPathwayItemAttempt(PathwayItemAttempt):
    # I'm not sure it would need a separate attempt type.
    pass