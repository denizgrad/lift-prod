from flask_restful import reqparse


def getArgs():
    """
    :return: object
    """
    parserGetArgs = reqparse.RequestParser()
    parserGetArgs.add_argument('filtercolumns', type=str, help='Belirtilen alan isimlerini çeker')
    parserGetArgs.add_argument('page', type=int, help='List Numarası')
    parserGetArgs.add_argument('limit', type=int, help='Listede gösterilecek kayıt sayısı')
    parserGetArgs.add_argument('orderby', type=str, help='Sıralama alanı')
    parserGetArgs.add_argument('type', type=int, help='Sıralama tipi')
    parserGetArgs.add_argument('fname_multi_type', type=str, help='Birden fazla alan adı karşılaştırması sorgu kuralı')
    parserGetArgs.add_argument('fname', type=str, help='Tablo alan adı')
    parserGetArgs.add_argument('ftype', type=str, help='Alan sorgulama kuralı')
    parserGetArgs.add_argument('fval', type=str, help='Tablo alan değer')
    parserGetArgs.add_argument('nin', type=str, help='Not in query values')
    parserGetArgs.add_argument('ninfname', type=str, help='Not in query field name')
    parserGetArgs.add_argument('in', type=str, help='In query values')
    parserGetArgs.add_argument('infname', type=str, help='In query field name')
    parserGetArgs.add_argument('getrelation', type=str, help='Get record with relation')
    parserGetArgs.add_argument('withtrash', type=bool, help='Get records with deleted')
    parserGetArgs.add_argument('withchilds', type=str, help='Get with childs')
    parserGetArgs.add_argument('text', type=str, help='Text field')
    parserGetArgs.add_argument('action', type=str, help='Get custom action name')
    parserGetArgs.add_argument('api_key', type=str, help='Requeired key')
    parserGetArgs.add_argument('raw_query',type=str, help="Raw Mongo Query String")
    parserGetArgs.add_argument('relation_object', type=str, help="Model class adı. Referans objesinin alanları ile arama yapmayı sağlar")
    parserGetArgs.add_argument('relation_field', type=str, help="Referans objesinin arama yapılacak alan adı")
    parserGetArgs.add_argument('relation_field_value', type=str, help="Referans objesinin arama yapılacak alanın eşleşme değeri")
    parserGetArgs.add_argument('related_field', type=str, help="Referans objesinin sonucuna göre ana objede arama yapılacak alan adı")
    parserGetArgs.add_argument('iexact_fields_query', type=str, help="Birden fazla alanı eşleştirmek için kullanılır. alan1:alan1value--alan2:alan2value")
    parserGetArgs.add_argument('iexact_fields_query_operator', default="$or", type=str, help="$or veya $and kabul eder")
    return parserGetArgs


def get_report_args():
    """
    :return: object
    """
    parserGetArgs = reqparse.RequestParser()
    parserGetArgs.add_argument('datefrom', type=int, help="[EPOCH date] Filtre başlangıç tarihi")
    parserGetArgs.add_argument('dateto', type=int, help="[EPOCH date] Filtre bitiş tarihi")
    parserGetArgs.add_argument('fname_multi_type', type=str, help='Birden fazla alan adı karşılaştırması sorgu kuralı')
    parserGetArgs.add_argument('fname', type=str, help='Tablo alan adı')
    parserGetArgs.add_argument('ftype', type=str, help='Alan sorgulama kuralı')
    parserGetArgs.add_argument('fval', type=str, help='Tablo alan değer')
    parserGetArgs.add_argument('limit', type=int, help='Listede gösterilecek kayıt sayısı')
    parserGetArgs.add_argument('currency_key', type=str, help='Para birimi belirtir')
    parserGetArgs.add_argument('tedarik_durumu', type=str, help='Tedarik durum')
    parserGetArgs.add_argument('action', type=str, help='Get custom action name')
    return parserGetArgs


def postArgs():
    """
    :return: object
    """
    parserPostArgs = reqparse.RequestParser()
    parserPostArgs.add_argument('data', type=dict)
    return parserPostArgs


def putArgs():
    """
    :return: object
    """
    parserPatchArgs = reqparse.RequestParser()
    parserPatchArgs.add_argument('data', type=dict)
    parserPatchArgs.add_argument('mongo_id', type=str, help='ObjectId')
    return parserPatchArgs


def deleteArgs():
    """
    :return: object
    """
    parserDeleteArgs = reqparse.RequestParser()
    return parserDeleteArgs