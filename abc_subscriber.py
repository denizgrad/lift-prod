from abc import ABC, abstractmethod


class ABCSubscriber(ABC):
    """
    Abstract base class for receiving notifications
    """
    @abstractmethod
    def notify(self):
        pass