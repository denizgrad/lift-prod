class PublisherUserOnCreate:
    """
    Publisher for notifying subscribers on new service admin user creating
    """
    def __init__(self):
        self.__new_user=None
        self.__subscribers=[]

    @property
    def new_user(self):
        """
        Publisher notifies subscribers about this user dict
        :return: new user dict
        """
        return self.__new_user

    @new_user.setter
    def new_user(self,user):
        """
        Set new_user dict and if not None notify all subscribers
        :param user: user dict
        :return: Void
        """
        self.__new_user=user
        if self.__new_user:
            self.notify_subscribers()

    def notify_subscribers(self):
        for subscriber in self.__subscribers :
            subscriber.notify()
    pass

    def add_subscriber(self,subscriber):
        self.__subscribers.append(subscriber)

    def remove_subscriber(self,subscriber):
        self.__subscribers.remove(subscriber)

