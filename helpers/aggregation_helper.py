
__all__ = ['get_mongo_unwind', 'get_mongo_lookup', 'get_ordered_dict_by_string']


def get_mongo_lookup(local_key, from_table_name, foreignkey, asname):
    return {
        '$lookup': {
            'from': from_table_name,
            'localField': local_key,  # current collection field
            'foreignField': foreignkey,  # relation table field
            'as': asname if asname else from_table_name,
        }
    }


def get_mongo_unwind(lookup_name, preserve_null_and_empty=True):
    return {
        '$unwind': {
            'path': '$' + lookup_name,
            'preserveNullAndEmptyArrays': preserve_null_and_empty
        }
    }


def get_ordered_dict_by_string(order_by_string):
    """ (string) -> dict

    :param order_by_string: Order_by string for mongodb "-key" or "key"
    :return: dict
    """
    key, val = order_by_string, 1
    if order_by_string.startswith('-'):
        key = order_by_string[1::]
        val = -1
    return {key: val}