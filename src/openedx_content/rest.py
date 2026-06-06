from datetime import datetime
from uuid import UUID

from django.conf import settings
from ninja import Field, FilterSchema, NinjaAPI, Schema


from .applets.publishing import api as publishing_api

rest_api = NinjaAPI()

class UserOut(Schema):
    username: str

class PublishableEntityOut(Schema):
    uuid: UUID
    entity_ref: str
    created: datetime
    created_by: UserOut | None


#@rest_api.get('/drafts')
#def get_drafts(request, learning_package: str):
#    return get_all_drafts()


@rest_api.get('/publishable_entities', response=list[PublishableEntityOut])
def get_publishable_entities(request, learning_package_ref: str):
    learning_package_obj = publishing_api.get_learning_package_by_ref(
        learning_package_ref
    )
    return publishing_api.get_publishable_entities(learning_package_obj.id)

