import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import DecimalField
from mongoengine import ReferenceField

from modules.analyzes.employment.kat_hesap_tipleri.models import KatHesapTipleri
from modules.analyzes.employment.pursantaj_oranlari.models import PursantajOranlari
from modules.organization.models import Organization


class EmploymentAnalysis(Document):

    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()
    analysis_date = StringField(required=True)

    _key_organization = ReferenceField(Organization, required=True)
    _key_kat_hesap_tipi = ReferenceField(KatHesapTipleri, required=True)
    _key_pursantaj_orani = ReferenceField(PursantajOranlari, required=True)

    birim_fiyat = DecimalField(required=True)
