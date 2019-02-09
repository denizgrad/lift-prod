from resources import app
from modules.notification.models import Notification
from flask_login import current_user

class Controller:
    def __init__(self):
        app.logger.debug('***Stok Malzeme crudJobs() called')

    @staticmethod
    def create(data):
        """
        Create notification record while setting message_no

        :param data:Object data used for kwargs
        :return: Notification Object
        """

        if Notification.objects.count() == 0:
            data["message_no"] = 1
        else:
            max_value = 0
            for notif in Notification.objects():
                if notif.message_no > max_value:
                    max_value = notif.message_no
            data["message_no"] = max_value + 1
        return Notification(**data).save()

    @staticmethod
    def create_mention_notification(message,mention):
        message_body = {'from':current_user.userid}
        notify_record = {'message_body':message_body,'related_to':mention,
                         'related_to_damage': message.related_to_damage.id,
                         'created_by': current_user.userid}
        return notify_record
# "Kullanıcı" adlı kullanıcı 5556677 numaralı dosyada yaptığı bir yorumda sizden bahsetti.