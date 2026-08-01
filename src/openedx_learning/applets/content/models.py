from django.db import models

from openedx_content.models_api import PublishableEntity

from ..contexts.models import LearningContext
from ....openedx_django_lib.fields import code_field


class LearningContent(models.Model):
    learning_context = models.ForeignKey(
        LearningContext,
        on_delete=models.PROTECT,
        null=False,
    )
    publishable_entity = models.ForeignKey(
        PublishableEntity,
        on_delete=models.SET_NULL,
        null=True,
    )
#    content_type = models.ForeignKey(
#
#    )

    usage_code = code_field(unicode=True)
