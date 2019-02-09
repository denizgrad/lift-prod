from datetime import datetime
from bson import ObjectId, errors
# App modelleri relation obje üzerinden arama yapabilmek için gerekli ***SİLMEYİN***
# method: prepare_relation_object_dict
from modules.organization.models import Organization
from modules.contact.models import Contact
from modules.message.models import Message
from modules.notification.models import Notification
from modules.user.models import User
from modules.location.models import Location
from abc_request_parser import ABCGetRequestParser
from resources import  app
from bson.json_util import dumps,loads
import re
from mongoengine.queryset.visitor import Q

class GetAllRequestParser(ABCGetRequestParser) :
    """
    HTTP request parser for GET calls which are used in table directives
    """
    def __init__(self,mongo_class,params,before_query_functions,after_query_functions):
        """
        Get all record with parameters used in querying

        :param mongo_class: mongo_engine class which will be queried
        :param params: get params
        1-fname : field name of query filter
        2-ftype : query option such as $gt,$lt... used with fname
        3-fval  : value of query filter
        4-ninfname : field name of nin query filter
        5-nin : value of nin query filter
        6-infname : field name of in query filter
        7-in : value of in query filter
        8-orderby : query order like ASC,DESC use with name beginning '+'(ASC) or '-'(DESC)
        9-getrelation : document relation which will be queried as objects separated with ','
        10-limit : how many records query will be returning -int
        11-page :  beginning offset for query -int
        12-raw_query : Mongo query
        :param before_query_functions: functions which will be run before query execution
        :param after_query_functions: functions which will be run after query execution
        """
        self.params = params
        self.mongo_class = mongo_class
        self.query_count = 0
        if before_query_functions is None :
            self.before_query_functions = []
        else:
            self.before_query_functions=before_query_functions
        if after_query_functions is None :
            self.after_query_functions=[]
        else :
            self.after_query_functions=after_query_functions

    def execute_query(self):
        app.logger.debug("*** params: {}".format(str(self.params)))
        # key word arguments for query filtering
        kwargs = {}
        # paginate defaults values used when page and limit params dont exist
        paginate_from = -1
        paginate_to = -1
        # check if page and limit params exits for pagination
        if self.params["page"] is not None and self.params["limit"] is not None:
            # paginate from parameter used for splicing beginning from REST parameters
            paginate_from = (self.params["page"] - 1) * self.params["limit"]
            # paginate end parameter used for splicing ending from REST parameters
            paginate_to = (self.params["page"]) * self.params["limit"]
        # check if field is GenericReferenceField
        reference_list = ["created_company",
                          'created_by',"related_to","related_to_damage","related_to_user", 'company',
                          '_id']

        if self.params["fname"] in reference_list :
            self.params.update({'fval':ObjectId(self.params['fval'])})
        # check if field is datetime
        if self.params["fname"] == 'created_date':
            self.params.update({'fval': datetime.utcfromtimestamp((int(self.params['fval'])/1000))})
        # key-word arguments(kwargs) used on query from REST parameters
        # check fname params in GET params
        if self.params["fname"] is not None and self.params["ftype"] == "regex":
            kwargs.update({self.params["fname"]+"__icontains": self.params["fval"]})
        if self.params["fname"] is not None and self.params["ftype"] == "eq" :
            app.logger.debug('***self.params["fname"] is not None and self.params["ftype"] == "eq" ')
            kwargs.update({self.params["fname"]: self.params["fval"]})
        # check ftype params in GET params
        if self.params["ftype"] is None or self.params["ftype"] == "eq" or self.params['ftype'] == "regex":
            pass
        else :
            # if ftype exist in params update key-words arguments dictionary and set in query filter
            kwargs.update({self.params["fname"]+"__"+self.params["ftype"]: self.params["fval"]})
        if self.params["infname"] is None :
            pass
        else :
            # check if infname is GenericReferenceField
            self.params["in"] = self.params["in"].split(",")
            app.logger.debug("***self.params['in']")
            app.logger.debug(self.params["in"])
            if self.params["infname"] in reference_list or self.params["infname"] == 'id':
                for i in range(len(self.params["in"])):
                    self.params["in"][i] = ObjectId(self.params["in"][i])
            app.logger.error("***self.params['in']")
            app.logger.error(self.params['in'])
            # if infname exist in params update key-words arguments dictionary and set in query filter
            kwargs.update({self.params["infname"]+"__in": self.params["in"]})
        if self.params["ninfname"] is None :
            pass
        else :
            # check if ninfname is GenericReferenceField
            self.params["nin"] = self.params["nin"].split(",")
            if self.params["ninfname"] in reference_list or self.params["ninfname"] == 'id':
                for nin_referance_value in self.params["nin"]:
                    nin_referance_value = ObjectId(nin_referance_value)
            # if ninfname exist in params update key-words arguments dictionary and set in query filter
            kwargs.update({self.params["ninfname"]+"__nin": self.params["nin"]})
        # if query needs filter on referancefield by referance attributes
        if self.params["relation_object"] is not None and self.params["related_field"] is not None:
            self.prepare_relation_object_dict(kwargs, reference_list)
        # if custom complex query requested prepare and update ``**kwargs``
        if self.params["iexact_fields_query"] is not None:
            iexact_fields_query = self.prepare_iexact_fields_query(reference_list)
        else:
            iexact_fields_query = False
        # if getrelation exits in params create relation_keys for getting relations as objects
        if self.params["getrelation"] is None:
            relation_keys = []
        else :
            relation_keys = self.params["getrelation"].split(",")
        # instantiate query with filter using kwargs
        if self.params["raw_query"] is None:
            app.logger.error("***kwargs : {}\n***iexact_fields_query: {}".format(str(kwargs), str(iexact_fields_query)))
            # if custom complex query requested prepare and update ``**kwargs``

            if iexact_fields_query is not False:
                self.query = self.mongo_class.objects(Q(**kwargs) & Q(__raw__=iexact_fields_query))
            else:
                self.query = self.mongo_class.objects(**kwargs)
        else:
            dict_raw_query = loads(self.params["raw_query"])
            for key in dict_raw_query.keys():
                if key in reference_list:
                    # raw_query alanları sadece değer karşılaştırmaları için kullanılmayabilir
                    # örnek olarak gelen değer şöyle olabilir: {'qr': {'$exists': False}}
                    if ObjectId.is_valid(dict_raw_query[key]):
                        dict_raw_query[key] = ObjectId(dict_raw_query[key])
                elif "date" in key and isinstance(dict_raw_query[key], dict):
                    for date_cond_key in dict_raw_query[key].keys():
                        prepared_ms = int(dict_raw_query[key][date_cond_key])/1000
                        dict_raw_query[key][date_cond_key] = datetime.utcfromtimestamp(prepared_ms)
            # if iexact_fields_query is not False:
            #     dict_raw_query.update(iexact_fields_query)
            if iexact_fields_query is not False:
                dict_raw_query.update(iexact_fields_query)
            self.query= self.mongo_class.objects(Q(__raw__=dict_raw_query) & Q(**kwargs))
        if self.params["orderby"] is not None:
            # instantiate query with order
            self.query = self.query.order_by(self.params["orderby"])
        self.query_count = len(self.query)
        if paginate_from > -1 and paginate_to > -1:
            # instantiate query with pagination
            self.query = self.query[paginate_from: paginate_to]
        load = []
        # convert QuerySet to json then to dict for modifying relation fields
        if len(self.query) > 0:
            load = loads(self.query.to_json())
        # app.logger.debug("***loads" + str(load))
        # for every query row there is a dict row ,enumerate and iterate over them
        for i, q in enumerate(load):
            # iterate over relation keys for finding relation fields
            for key in relation_keys:
                try:
                    app.logger.debug(
                        "***key" + key)
                    # app.logger.debug("***(getattr(self.query[i],key).to_mongo())"+str(getattr(self.query[i],key).to_mongo()))
                    # set 'key' reference field object with lazy loading from object field
                    q[key] = (getattr(self.query[i],key).to_mongo())
                except AttributeError as e:
                    app.logger.debug('***Key cannot be found')
                    app.logger.exception(e)
        # set self.query as load for returning it at prepare_result
        self.query=load
    def prepare_result(self):
        # return format should be as {"result":".....","list":QUERYRESULT as json,"totalRecord":RECORDCOUNT}
        # for table directive
        app.logger.debug('***len query'+str(len(self.query)))
        return {"result": "Success", "list": dumps(self.query), "totalRecord": self.query_count}, 200

    def prepare_relation_object_dict(self, query_dict, reference_list):
        """
        Update query **kwargs by related_object attribute value if relation_object is exists in globals()
        :param query_dict: {dict} query filter dict (**kwargs)
        :param reference_list: {list} reference_list for the which value need to convert ObjectId
        :return: Returns False when any exception occured which is known
        """
        try:
            relation_object = globals()[self.params['relation_object'].capitalize()]
        except KeyError as e:
            app.logger.error("*** KeyError:: relation_object not found")
            app.logger.exception(e)
            return False
        # if relation_field and value is not none check for filter
        # if relation_field or value is none get all ids in relation_object
        if self.params["relation_field"] is not None and self.params["relation_field_value"] is not None:
            if self.params["relation_field"] in reference_list:
                # If field in referance_list and value is not valid for ObjectId log exception and return False
                try:
                    self.params["relation_field_value"] = ObjectId(self.params["relation_field_value"])
                except Exception as e:
                    app.logger.error("*** bson.errors.InvalidId:: '{}' is not a valid ObjectId".format(self.params["relation_field_value"]))
                    app.logger.exception(e)
                    return False
            ids = relation_object.objects(**{self.params["relation_field"]+"__icontains": self.params["relation_field_value"]}).only("id")
        else:
            ids = relation_object.objects.only("id")
        # update query_dict filter
        query_dict.update({self.params["related_field"]+"__in": ids})

    def prepare_iexact_fields_query(self, reference_list):
        """
        Update query **kwargs by ``iexact_fields_query`` attribute value
            ``iexact_fields_query`` value should be like "field1:field1value--field2:field2value..."
        :param reference_list: {list} reference_list for the which value need to convert ObjectId
        :return dict
            {"$or": [{"field1":"field1value"}, {field2:"field2value"}]}
            operator could be "$and" instead of "$or"
        """
        app.logger.debug("*** prepare_iexact_fields_query fired")
        raw_operator = "$and" if self.params["iexact_fields_query_operator"] == "$and" else "$or"
        query_list = []
        # splite string by fields seperator "--"
        splitted_fields = self.params["iexact_fields_query"].split("--")
        for field_string in splitted_fields:
            try:
                # splite field_string by seperator ":"
                # and get field name which is first index and field value which is last index
                splitted_field = field_string.split(":")
                # Check field is need to convert to ObjectId
                if splitted_field[0] in reference_list or splitted_field[0] == "_id":
                    query_list.append({splitted_field[0]: ObjectId(splitted_field[1])})
                else:
                    query_list.append({splitted_field[0]: splitted_field[1]})
            except errors.InvalidId as bsonError:
                app.logger.error("{}.prepare_iexact_fields_query occured an bson.errors.InvalidId error".format(self.__class__.__name__))
                app.logger.exception(bsonError)
                raise bsonError
            except Exception as e:
                app.logger.error("{}.prepare_iexact_fields_query occured an exception".format(self.__class__.__name__))
                app.logger.exception(e)
                pass
        if len(query_list) > 0:
            return {raw_operator: query_list}
        else:
            return False


    @property
    def before_query_functions(self):
        return self.__before_query_functions

    @property
    def after_query_functions(self):
        return self.__after_query_functions

    @before_query_functions.setter
    def before_query_functions(self,function_list):
        self.__before_query_functions = function_list

    @after_query_functions.setter
    def after_query_functions(self,function_list):
        self.__after_query_functions = function_list


