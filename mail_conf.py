from resources import app,mail
from flask import render_template
from flask_mail import Message
from async_thread import async




#UNICODE CHAR HEXS
# İ= \u0130 Ş= \u015e Ç= \u00c7 Ü= \u00dc ı=\u0131 ş=\u015f ğ=\u011f Ğ= \u011e



def generateKullanıcıAcildiNotificationBody(user):
    app.logger.debug('*** generateKullanıcıAcildiNotificationBody fired')

    mailBody = str(user.first_name)+" "+str(user.last_name) +" \u0130S\u0130ML\u0130 KULLANICI TANIMLANMI\u015eTIR. YETK\u0130LER\u0130 "+str(user.permissions)

    app.logger.debug("*** generateKullanıcıAcildiNotificationBody ended")
    return mailBody


def generateSifreUnuttumNotificationBody(user):
    app.logger.debug('*** generateSifreUnuttumNotificationBody fired')
    mailBody = str(user.first_name)+" "+str(user.last_name) +" isimli  kullan\u0131c\u0131 \u015fifresi s\u0131f\u0131rlanm\u0131şt\u0131r.A\u015fa\u011f\u0131daki tu\u015f ile yeni \u015fifre oluşturabilirsiniz."

    app.logger.debug("*** generateSifreUnuttumNotificationBody ended")
    return mailBody


@async
def sendTemplateEmail(receiver,title,body,subject):
    """
    Async mail sender method
    :param receiver: list
    :param title: string
    :param body: ?any?
    :param subject: string
    :return: bool
    """
    app.logger.debug("*** sendTemplateEmail fired")
    with app.app_context():
        app.logger.debug("*** sendTemplateEmail mail preparing as async")
        msg = Message(subject,
                      sender=("Softnec Bilgi", "bilgi@soft-nec.com"),
                      recipients=receiver)
        msg.html = render_template('Email-Template.html', title=title, body=body)
        app.logger.debug("*** Mail Send to :" + str(receiver))
        try :
            mail.send(msg)
        except Exception as e:
            app.logger.exception("sendTemplateEmail Send Exception :" )
            app.logger.exception(e)
    return True


@async
def sendForgetPasswordEmail(receiver,title,body,subject,link):
    with app.app_context():
        app.logger.debug("*** sendForgetPasswordEmail mail preparing as async")
        msg = Message(subject,
                      sender=("Softnec Bilgi", "bilgi@soft-nec.com"),
                      recipients=receiver)
        msg.html = render_template('Email-ForgetPassword.html', title=title, body=body,link=link)
        app.logger.debug("*** sendForgetPasswordEmail Send to :" + str(receiver))
        try :
            mail.send(msg)
        except Exception as e:
            app.logger.exception("***sendForgetPasswordEmail Send Exception :" )
            app.logger.exception(e)
    return True


def send_user_created_by_owner_email(created_user, owner_full_name, subject, jwt, send_async=True):
    """
    Şirket yöneticisi tarafından yeni kullanıcı oluşturulduğunda,
        kullanıcının şifresini tanımlaması için davetiye bildirimi yapar
    :param created_user: {User} Oluşturulan kullanıcı kaydı
    :param owner_full_name: {str} İşemi yapan kullanıcının tam adı
    :param subject: Email bildirim başlığı
    :return: {bool}
    """
    with app.app_context():
        link_string = app.config.get("HOST_NAME") + app.config.get("PASSWORD_RECOVERY_ENDPOINT") + jwt.decode('UTF-8')
        msg = Message(subject,
                      sender=("Softnec Bilgi", "bilgi@soft-nec.com"),
                      recipients=[created_user.email])
        msg.html = render_template(
            'email_templates/user_created_by_owner.html',
            owner_full_name=owner_full_name,
            created_user=created_user,
            link=link_string
        )
        if send_async is True:
            send_email_asynchronous(msg)
        else:
            try:
                mail.send(msg)
            except Exception as e:
                app.logger.exception("*** sendUserCreatedByOwnerEmail Send Exception :" )
                app.logger.exception(e)
            return True


@async
def send_email_asynchronous(message_object):
    """
    Eşzamanlı olmayan email gönderme işlemi yapar
    :param message_object: {Message} Mail içeriği Message sınıfından oluşmalıdır
    """
    with app.app_context():
        try:
            mail.send(message_object)
        except Exception as e:
            app.logger.exception("*** send_email_asynchronous occurred an exception;")
            app.logger.exception(e)
        return True
