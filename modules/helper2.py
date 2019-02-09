import json
import re

from modules.permission.constants import EnumPermission
from resources import app
from datetime import datetime, timedelta
from bson import json_util
from bson.objectid import ObjectId
from flask import session
import os



class helper():
    def __init__(self):
        self.formatString = '%d.%m.%Y %H:%M:%S'

    def listModules(self):
        modules = set()
        try:
            import glob

            for module in glob.iglob(os.path.dirname(__file__) + '/**', recursive=True):
                #     print(filename)
                # for module in os.listdir():
                if module[-3:] == '.py' or module[-4:] == '.pyc' or module[:2] == '__':
                    continue
                hier = module.split("/")
                # if re.search("enginespeed", module, re.IGNORECASE) :
                module_add = hier[len(hier) - 1]
                if not module_add.startswith("__") and module_add != "":
                    modules.add(module_add)
            return modules
        except Exception as e:
            print(str(e))
        return None

    def listActions(self):
        actions = ['get', 'post', 'put', 'delete']
        return actions

    def listRoles(self):
        roles = [e.value for e in EnumPermission]
        return roles

    def isAdmin(self):
        return session['current_user_id'] == "admin"

    def epoch_time_to_datetime(self, epoch):
        """
        Convert epoch time to datetime object
        :param epoch: int | time as microseconds
        :return: datetime
        """
        return datetime.fromtimestamp(epoch/1000)

    def stringIdToObjectId(self, stringId):
        """
        :param stringId: stringID | mongoId of any collection
        :return: ObjectId
        """
        # TODO:deniz: Gereksiz ve classlarda okunabilirliği azaltıryor. Bunun yerine direk bson.ObjectId kullanalım.
        return ObjectId(stringId)

    def get_month_name_by_number(self, month_number):
        month_map = [
            '', 'Ocak', 'Şubat', 'Mart', 'Nisan',
            'Mayıs', 'Haziran', 'Temmuz', 'Ağustos',
            'Eylül', 'Ekim', 'Kasım', 'Aralık'
        ]
        return month_map[month_number]

    def find_in_between(self,string,first,last):
        """
        Find the substring between tokens
        :param string: string to search
        :param first: first token of substring
        :param last: last token of substring
        :return: substring
        """
        try:
            start = string.index(first) + len(first)
            end = string.index(last, start)
            return string[start:end]
        except ValueError:
            return None

    def parse_message_mention_tags(self,string):
        keyword = 'mongoid'
        quotation = '"'
        catched_list = []
        try:
            splitted_list = string.split('[')
        except AttributeError as e:
            splitted_list = []
            app.logger.debug('***There is no string to split')
            app.logger.exception(e)
        for splitted in splitted_list :
                try:
                    keyword_start_index = splitted.index(keyword)
                    catched = self.find_in_between(splitted[keyword_start_index:],quotation,quotation)
                    if catched:
                        catched_list.append(ObjectId(catched))
                except ValueError as e:
                    app.logger.debug('*** Cannot find keyword')
                    app.logger.exception(e)
        return catched_list
