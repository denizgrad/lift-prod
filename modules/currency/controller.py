from resources import app
from get_all_request_parser import GetAllRequestParser
from pprint import pprint
from flask import Response, session

from modules.currency.models import Currency, Parity
from modules.user.models import User
from modules.organization.models import Organization
from modules.currency.utils import Tcmb
from bson.json_util import dumps

class Controller:

    def __init__(self):
        app.logger.debug('*** {} class called'.format(self.__class__.__name__))

    def get_all(self, get_args):
        """
        :param get_args: list
        :return: dict
        """
        data = Currency.objects()

        data_to_go = dumps({'data': [ob.to_mongo() for ob in data]})
        return Response(data_to_go, status=201, mimetype='application/json')

    def get_one(self, mongo_id, get_args=None):
        """
        :param mongo_id: string
        :param get_args: dict | optional. Default = None
        :return: dict
        """
        # add mongo id as get_args params for querying
        get_args.update({"fname": "id", "fval": mongo_id})
        # Instantiate GetAllRequestParsef for Currency class with get_args
        request_parser = GetAllRequestParser(Currency, get_args, None, None)
        # parse arguments and return result
        return request_parser.run()

    def create_currency(self, data):
        """
        Create a new currency record
        :param data: dict
        :return: dict
        """
        pprint(data)

        return Currency(**data).save()

    def create_parity(self, data):
        """
        Create a new parity record
        :param data: dict
        :return: dict
        """
        data['_key_currency'] = Currency.objects(code=data["_key_currency"]).first().id
        return Parity(**data).save()

    def update_rates(self):
        """
        Update Parity and currency
        :param data: dict
        :return: dict
        """
        app.logger.warning("*** update_rates fired")
        util_tcmb = Tcmb()
        rates = util_tcmb.get_rates()
        codes = list(rates.keys())
        currencies = []
        try:
            currencies = Currency.objects(code__in=codes).only('code')
        except Exception as e:
            app.logger.error("*** update_rates occurred an exception on fetching currencies: {}".format(e))
        # TODO:Niyazi: Currency bilgisini organizasyon bazlı tutmamızın bir anlamı yok. Bunu global tutalım
        # _key_organization = None
        # if session['current_org_id']:
        #     _key_organization = Organization.objects.get(id=session['current_org_id'])
        #
        # _key_user = None
        # if session["current_user_id"]:
        #     _key_user = User.objects.get(id=session["current_user_id"])

        # remove exist codes
        for _currency in currencies:
            codes.remove(_currency.code)

        # create not exist currency
        for code in codes:
            # rates[code]["_key_user"] = _key_user
            self.create_currency(dict(code=code, name=rates[code]['name']))

        # create new parity
        for code in rates.keys():
            create_dict = dict(
                _key_currency=code,
                ask_price=rates[code]["BanknoteSelling"],
                bid_price=rates[code]["BanknoteBuying"]
            )
            self.create_parity(create_dict)
        app.logger.warning("*** update_rates done")
        return True

    def delete(self, mongoid):
        """
        Delete a record with description
        :param mongoid: string
        :param deleted_desc: string
        :return: dict
        """
        return Currency(id=self.helper.stringIdToObjectId(mongoid)).delete()

    def check_Currency_exist(self, Currency_name):
        """
        Check if any Currency exist with given Currency name
        :param Currency_name: Name of the Currency
        :return: if exists True , else False
        """
        Currency_records = Currency().objects(name=Currency_name)
        if len(Currency_records) > 0:
            return True
        else:
            return False


