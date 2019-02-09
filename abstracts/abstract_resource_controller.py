import datetime
from abc import ABCMeta
from flask import session
from bson import ObjectId, json_util
from mongoengine.fields import ReferenceField, ObjectIdField
from mongoengine.errors import LookUpError, DoesNotExist

from resources import app
from interfaces.resource_controller import ResourceController
from helpers.http_helper import HttpHelper


__all__ = ['AbstractResourceController']


class AbstractResourceController(ResourceController, metaclass=ABCMeta):
    """
        Usage:
            class SomeController(AbstractResourceController):
                def __init__(self):
                    #  Init subclass __init__

                    #  Property `main_model` Should be a reference of mongoengine.Document
                    #  Property `default_kwargs` Default kwargs will affect your all get and show filter queries
                    self.main_model = HERE_YOUR_DB_MODEL
                    self.default_kwargs = dict()
    """

    def get(self, get_args):
        """
        Default query handler for your list queries
        :param {dict} get_args: Query params
        :return: (db_cursor, int)
        """
        include = get_args.get('include', None)
        get_args = self.prepare_paginator_args(get_args)
        get_args['query'] = self.handle_query_dict(get_args['query'])
        result, total_count = self.run_paginator_query(get_args)
        # Reference alanlara erişim istenmiş mi kontrol et
        result = self.load_required_reference_fields(document_list=result, include=include)
        return result, total_count

    def show(self, document_id, get_args):
        include = get_args.get('include', None)
        query = dict(id=ObjectId(document_id))
        query = self.handle_query_dict(query)
        result_id = document_id
        result = self.main_model.objects(**query)
        if result:
            if include:
                # Reference alanlara erişim istenmiş mi kontrol et
                result = self.load_required_reference_fields(document_list=result, include=include)[0]
            else:
                result = result.first().to_mongo()
        return result, result_id

    def update(self, mongoid, update_data):
        if not isinstance(update_data, dict):
            raise TypeError('*** Update data should be dict type not: {}'.format(type(update_data)))
        query_dict = dict(id=mongoid)
        self.add_default_filters(query_dict)
        model_dict = self.main_model.objects(**query_dict).first()
        if model_dict:
            # Frontend tarafından gelebilecek olan `$` ile başlayan alanları sil
            print("update_data: {}".format(update_data))
            HttpHelper.clear_invalid_values(update_data)
            self.add_default_update_data(update_dict=update_data)
            # Assign update_data values to document
            for key, value in update_data.items():
                lookup_field = self.lookup_model_field(key)
                if self.is_reference_field(lookup_field) or self.is_object_id_field(lookup_field):
                    value = ObjectId(value)
                model_dict[key] = value
            return model_dict.save()
        raise DoesNotExist('Kayıt bulunamadı veya erişim yetkiniz yok')

    def create(self, create_data):
        if not isinstance(create_data, dict):
            raise TypeError('*** Create data should be dict type not: {}'.format(type(create_data)))
        # Frontend tarafından gelebilecek olan `$` ile başlayan alanları sil
        HttpHelper.clear_invalid_values(create_data)
        self.add_default_create_data(create_dict=create_data)
        print("create data: {}".format(create_data))
        return self.main_model(**create_data).save()

    def delete(self, document_id, delete_args):
        record = self.main_model.objects(id=document_id).first()
        if not record:
            raise DoesNotExist('Kayıt bulunamadı veya erişim yetkiniz yok')
        return record.delete(signal_kwargs=delete_args)

    def bulk_create(self, bulk_list):
        results = {'has_error': False, 'errors': [], 'created_count': 0}
        for index, create_data in enumerate(bulk_list):
            try:
                print("create data: {}".format(create_data))
                self.create(create_data)
                results['created_count'] += 1
            except Exception as e:
                print("data: {}".format(create_data))
                app.logger.error("*** {}.bulk_create occurred an exception".format(self.main_model.__name__, e.with_traceback))
                app.logger.exception(e)
                results['has_error'] = True
                results['errors'].append({'index': index, 'detail': e.args})
        return results

    @classmethod
    def prepare_paginator_args(cls, get_args):
        return HttpHelper.prepare_paginator_args(get_args)

    def handle_query_dict(self, query_dict):
        self.add_default_filters(filter_dict=query_dict)
        return self.find_reference_fields_and_convert(query_dict)

    def run_paginator_query(self, get_args):
        return HttpHelper.run_paginator_query(self.main_model, get_args)

    def find_reference_fields_and_convert(self, search_dict):
        """ (dict) -> dict

        Dict objesi içinde ObjectId değerinde olması gereken alanları ObjectId formatına çevirir

            Usage:
                self.find_reference_fields_and_convert(dict(_key_owner_name='ObjecId_AS_STR_TYPE'))
                ->
                dict(_key_owner_name=ObjectId('...'))
        """
        for field_name in search_dict.keys():
            if not field_name.startswith('$') and isinstance(search_dict[field_name], str):
                try:
                    lookup_field = self.lookup_model_field(field_name)
                    # If field is instance ReferenceField or ObjectIdField then convert string value to ObjectId
                    if self.is_reference_field(lookup_field) or self.is_object_id_field(lookup_field):
                        search_dict[field_name] = ObjectId(search_dict[field_name])
                except LookUpError:
                    # Field is not part of query
                    # del search_dict[field_name]
                    pass
                except IndexError:
                    pass
        return search_dict

    def lookup_model_field(self, field_name):
        """
        Find field on document sheme by name
        """
        return self.main_model._lookup_field(field_name)[0]

    @classmethod
    def is_reference_field(cls, lookup_field):
        return isinstance(lookup_field, ReferenceField)

    @classmethod
    def is_object_id_field(cls, lookup_field):
        return isinstance(lookup_field, ObjectIdField)

    @classmethod
    def load_required_reference_fields(cls, document_list, include):
        """
        Load required related collections for list of document
        :param {MongoCursor} document_list:
        :param {str} include: reference fields name list seperated with `,` -> field_1,field_2,field_3
        :return: list|MongoCursor
        """
        if isinstance(include, str):
            doc_list = json_util.loads(document_list.to_json())
            for index, record in enumerate(doc_list):
                for field in include.split(','):
                    try:
                        doc_list[index][field] = getattr(document_list[index], field).to_mongo()
                    except AttributeError:
                        pass
            return doc_list
        return document_list

    def add_default_filters(self, filter_dict):
        try:
            filter_dict.update(self.default_kwargs)
        except AttributeError:
            filter_dict.update(dict(_key_organization=session["current_org_id"]))

    def add_default_create_data(self, create_dict):
        try:
            create_dict.update(self.default_create_data)
        except AttributeError:
            create_dict.update(dict(
                _key_organization=session["current_org_id"],
                _key_created_user=session["current_user_id"],
                _key_owner_user=session["current_user_id"]
            ))

    def add_default_update_data(self, update_dict):
        try:
            update_dict.update(self.default_create_data)
        except AttributeError:
            update_dict.update(dict(
                _last_modified_date=datetime.datetime.utcnow(),
                _key_last_modified_user=session["current_user_id"]
            ))
