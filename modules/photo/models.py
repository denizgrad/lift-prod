import datetime

from mongoengine import Document, StringField, DateTimeField, ReferenceField

from modules.organization.models import Organization
from modules.message.models import Message
from modules.user.models import User
from resources import db


class Photo(Document):
    """
    For storing photo related to damage,user object and embedded acceptance,delivery objects
    ===Acceptance===
    km_photo
    chassis_photo
    toolkit_photo
    spare_tire_photo
    jack_photo
    # hasar fotoları
    damages_photos
    # talep dışı hasarların fotoları
    demand_off_damage_photos
    # diğer fotolar
    other_photos
    ===Damage===
    photos
    ===Delivery===
    km_photo
    acceptance_photo
    toolkit_photo
    spare_tire_photo
    jack_photo
    ==User==
    profile_pic
    ===Company===
    company_photo
    #===Flow===
    flowphoto
    """


    file_name = StringField()
    title = StringField()
    description = StringField()
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    created_by = ReferenceField(User)
    related_to_user = ReferenceField(User)
    related_to_message = ReferenceField(Message)
    related_to_field = StringField()
    related_to_company = ReferenceField(Organization)
    # is needed for allowing inheritance for child classes
    # meta = {'allow_inheritance': True}
