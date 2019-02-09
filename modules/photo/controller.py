import os

from bson import ObjectId

from .models import Photo
from resources import app
from flask_login import current_user
from PIL import Image


class Controller:

    def __init__(self):
        app.logger.debug('*** {} class called'.format(self.__class__.__name__))


    def create(self, data):
        """
        Create a new record
        :param data: dict
        :return: dict
        """
        photo_record = Photo(**data)
        photo_record.created_by = current_user.userid
        return photo_record.save()

    def update(self, mongoid, data):
        """
        Update a record
        :param mongoId: string | mongoID
        :param data: dict
        :return: dict
        """


    def delete(self, mongoid):
        """
        Delete a record with description
        :param mongoid: string
        :param deleted_desc: string
        :return: dict
        """
        photo_record = Photo.objects(id=ObjectId(mongoid)).first()
        try:
            os.remove(app.config['UPLOAD_FOLDER']+photo_record.file_name)
            photo_record.delete()
        except Exception as e:
            app.logger.exception(e)
            return False
        return True

    @staticmethod
    def save_image_by_ratio(image_path=None, base_width='s'):
        """
        STATIC VOID METHOD
        Resim dosyasını farklı boyutta ratio oranını göz önüne alanarak genişlik değeri ``base_width`` olacak şekilde oluştur
        :param image_path: {str} Resim dosyasının konumu
        :param base_width: {str} Resim dosyasının genişlik boyutunu belirler
                                 Alabileceği değerler ["s", "m"]
        """
        if os.path.isfile(str(image_path)) and app.testing is not True:
            if base_width == 's':
                base_width = 64
            elif base_width == 'm':
                base_width = 128
            else:
                base_width = 128
            fname, ftype = image_path.split('.')
            new_file_name = "{}x{}.{}".format(fname, str(base_width), ftype)
            if os.path.isfile(new_file_name) is False:
                img = Image.open(image_path)
                wpercent = (base_width / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((base_width, hsize), Image.ANTIALIAS)
                img.save(new_file_name)
