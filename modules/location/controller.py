from bson import ObjectId
from flask_login import current_user

from get_all_request_parser import GetAllRequestParser
from modules.location.models import Location


class LocationController():
    def get_all(self, get_args):
        """
        :param get_args: list
        :return: dict
        """
        self.logger.debug('*** {}.get_all method fired with args: {}'.format(self.__class__.__name__, str(get_args)))
        # Instantiate GetAllRequestParsef for Company class with get_args
        request_parser = GetAllRequestParser(Location, get_args, None, None)
        # parse arguments and return result
        return request_parser.run()
        pass

    def get_one(self, mongoid, get_args=None):
        """
        :param mongoid: string
        :param get_args: dict | optional. Default = None
        :return: dict
        """
        # add mongo id as get_args params for querying
        get_args.update({"fname": "id", "fval": mongoid})
        # Instantiate GetAllRequestParsef for Company class with get_args
        request_parser = GetAllRequestParser(Location, get_args, None, None)
        # parse arguments and return result
        return request_parser.run()

    def create(self, data):
        """
        Create a new record
        :param data: dict
        :return: dict
        """

        damage_record = Location(**data)
        # set current user company as service company
        damage_record.created_by = current_user.userid
        return damage_record.save()

    def delete(self, mongoid):
        """
        Delete a record with description
        :param mongoid: string
        :param deleted_desc: string
        :return: dict
        """
        return Location(id=ObjectId(mongoid)).delete()