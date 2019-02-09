from flask_restful import reqparse


def get_args():
    """
    Get query parameters on request
    :return: RequestParser
    """
    parser_get_args = reqparse.RequestParser()
    parser_get_args.add_argument('text_search', type=str, help="Set wants to perform text search")
    parser_get_args.add_argument('include', type=str, help="Require reference field details")
    parser_get_args.add_argument('query', type=str, help="Db query string", default='{}')
    parser_get_args.add_argument('order', type=str, help="Order type -created_at or created_at", default='-id')
    parser_get_args.add_argument('page', type=int, help="Pagination page number", default=1)
    parser_get_args.add_argument('limit', type=int, help="Pagination limit", default=15)
    # TODO: only ve exclude yapısını performans nedenleri ile ilerleyen süreçlerde dahil etmeliyiz
    # parser_get_args.add_argument('only', type=str, help='Load only a subset of this document’s fields.')
    # parser_get_args.add_argument('exclude', type=str, help='Opposite to .only(), exclude some document’s fields.')
    return parser_get_args


def post_put_args():
    """
    :return: RequestParser
    """
    parser_post_args = reqparse.RequestParser()
    parser_post_args.add_argument('data', type=dict)
    return parser_post_args


def delete_args():
    """
    :return: RequestParser
    """
    parser_delete_args = reqparse.RequestParser()
    parser_delete_args.add_argument('forceDelete', type=str)
    parser_delete_args.add_argument('deleted_desc', type=str, help='Why deleted description')
    return parser_delete_args
