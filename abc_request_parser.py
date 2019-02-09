from abc import ABC,abstractmethod,abstractproperty
from resources import app

class ABCGetRequestParser(ABC):
    """
    Abstract Base Class for handling get requests from REST calls
    """

    @abstractmethod
    def execute_query(self):
        """
        Execute query and return result
        :return: response from query execution
        """
    @abstractmethod
    def prepare_result(self):
        """
        Prepare query result as expected HTTP response
        :return: Response body returned in HTTP response
        """
    def run(self):
        """
        Main method for handling request
        :return: HTTP response according to execution of query
        """

        for func in self.before_query_functions :
            try:
                func(self)
            except Exception as e:
                app.logger.debug("Get Request Parser run before_query_functions exception :")
                app.logger.exception(e)
        self.execute_query()
        for func in self.after_query_functions :
            try:
                func(self)
            except Exception as e:
                app.logger.debug("Get Request Parser run after_query_functions exception :")
                app.logger.exception(e)
        return self.prepare_result()

    @property
    @abstractmethod
    def before_query_functions(self):
        """
        list of functions to run before query execution
        :return: list of functions
        """
        pass

    @before_query_functions.setter
    @abstractmethod
    def before_query_functions(self,function_list):
        pass

    @property
    @abstractmethod
    def after_query_functions(self,function):
        """
                list of functions to run after query execution
                :return: list of functions
                """
        pass

    @after_query_functions.setter
    @abstractmethod
    def after_query_functions(self,function_list):
        pass