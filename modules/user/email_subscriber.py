from abc_subscriber import ABCSubscriber
from mail_conf import sendTemplateEmail


class EmailSubscriber(ABCSubscriber):
    """
    Subscriber for getting changes in user records by email
    """
    def __init__(self,receiver,publisher):
        """
        initialize with email of the receiver and new created user object
        :param receiver: string email of the receiver
        :param publisher: publisher object
        """
        self.receiver = receiver
        self.publisher = publisher

    def notify(self):
        sendTemplateEmail([self.receiver],'OtoServis-Yeni Kullanıcı Onay Gerekli','{} emaili ile yeni servis yönetici kullanıcısı tanımlanmıştır.'
                                                                '\n Detayları görmek için sisteme giriniz.'.format(self.publisher.new_user['email']),'Yeni Kullanıcı Onay Gerekli')
