
from .models import Message
from resources import app
from ..helper2 import  helper as helper
from flask_login import current_user
import get_all_request_parser
from flask import session

class Controller:

    def __init__(self):
        app.logger.debug('*** {} class called'.format(self.__class__.__name__))
        self.help = helper()


    def get_all(self, get_args):
        """
        :param get_args: list
        :return: dict
        """
        self.logger.debug('*** {}.get_all method fired with args: {}'.format(self.__class__.__name__, str(get_args)))
        # Instantiate GetAllRequestParsef for Company class with get_args
        request_parser = get_all_request_parser(Message, get_args, None, None)
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
        request_parser = get_all_request_parser(Message, get_args, None, None)
        # parse arguments and return result
        return request_parser.run()

    def create(self, data):
        """
        Create a new record
        :param data: dict
        :return: dict
        """
        message_record = Message(**data)
        # set current user company as service company
        message_record.created_by = current_user.userid
        # set mentions from message's text field
        message_record.mentions = self.help.parse_message_mention_tags(message_record.text_body)

        if 'qr' in session:
            message_record.qr = session['qr']
        else:
            message_record.qr = False

        message_record = message_record.save()

        return message_record

    def update(self, mongoid, data):
        """
        Update a record
        :param mongoId: string | mongoID
        :param data: dict
        :return: dict
        """
        message_record=Message(**data)
        message_record.id=helper.stringIdToObjectId(mongoid)
        message_record.save()
        return message_record

    def delete(self, mongoid):
        """
        Delete a record with description
        :param mongoid: string
        :param deleted_desc: string
        :return: dict
        """
        return Message(id=self.helper.stringIdToObjectId(mongoid)).delete()



