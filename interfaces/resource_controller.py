from abc import ABCMeta, abstractmethod
from mongoengine import Document


class ResourceController(object, metaclass=ABCMeta):
    """
        @abstractmethod
        def __init__(self):
            #  Init subclass __init__

            #  Property `main_model` Should be a reference of mongoengine.Document
            #  Property `default_kwargs` Default kwargs will affect your all get and show filter queries
            self.main_model = None
            self.default_kwargs = dict()
            self.default_create_data = dict()
    """

    @property
    def main_model(self):
        return self.__main_model

    @main_model.setter
    def main_model(self, main_model):
        assert issubclass(main_model, Document), 'main_model must be subclass of `mongoengine.Document`'
        self.__main_model = main_model

    @property
    def default_kwargs(self):
        return self.__default_filter_kwargs if isinstance(self.__default_filter_kwargs, dict) else dict()

    @default_kwargs.setter
    def default_kwargs(self, value):
        assert isinstance(value, dict), 'default_kwargs should be dict type but got: {}'.format(type(value))
        self.__default_filter_kwargs = value

    @property
    def default_create_data(self):
        return self.__default_create_data if isinstance(self.__default_create_data, dict) else dict()

    @default_create_data.setter
    def default_create_data(self, value):
        assert isinstance(value, dict), 'default_create_data should be dict type but got: {}'.format(type(value))
        self.__default_create_data = value

    @property
    def default_update_data(self):
        return self.__default_update_data if isinstance(self.__default_update_data, dict) else dict()

    @default_update_data.setter
    def default_update_data(self, value):
        assert isinstance(value, dict), 'default_create_data should be dict type but got: {}'.format(type(value))
        self.__default_update_data = value

    @property
    def is_safe_delete_avaible(self):
        try:
            return self.__is_safe_delete_avaible
        except AttributeError:
            return False

    @is_safe_delete_avaible.setter
    def is_safe_delete_avaible(self, value):
        self.__is_safe_delete_avaible = True if value is True else False

    @abstractmethod
    def get(self, get_args):
        """ (dict) -> list
        Query documents and return result
        :param {dict} get_args:  Query parameters
        :return: list|None
        """
        pass

    @abstractmethod
    def show(self, document_id, get_args):
        """ (str) -> dict
        Query documents by id and return result
        :param {str} document_id: Record database id
        :param {dict} get_args:  Query parameters
        :return: document
        """
        pass

    @abstractmethod
    def create(self, create_data):
        """ (dict) -> document
        Insert a new document
        :param {dict} create_data: New document fields
        :return: document
        """
        pass

    @abstractmethod
    def update(self, document_id, update_data):
        """ (str, dict) -> bool
        Update a document by id
        :param document_id: Document id which will be updated
        :param update_data: Update content
        :return: bool
        """
        pass

    @abstractmethod
    def delete(self, document_id, delete_args):
        """ (str, dict) -> bool
        Delete a document by id
        :param document_id: Document id which will be deleted
        :param delete_args: Delete signal_args
        :return: bool
        """
        pass

    @abstractmethod
    def bulk_create(self, bulk_list):
        """ (list(dict(), dict())) -> bulk_list

        :param {list} bulk_list: Bulk create list
        :return: dict
        """
        pass

    # @abstractmethod
    # def get_total_record(self, query, with_limit_and_skip=False):
    #     """ (dict, bool) -> int
    #     Get total record in document
    #     :param query: Document raw_filter
    #     :param with_limit_and_skip: take any :meth:`limit` or
    #         :meth:`skip` that has been applied to this cursor into account when
    #         getting the count
    #     :return: int
    #     """
    #     pass
