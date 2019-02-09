import os
from bson import json_util
from flask_restful import request
from resources import app


class ControllerAdminJobs:

    def run_photo_resize_job(self):
        """
        Photo modelinde kayıtlı ve sistem UPLOAD_FOLDER içersindeki fotoğraflar için;
            ``small (s)`` ve ``medium (m)`` boylarında kopyalarını oluşturmayı sağlar
        :return: {tuple}
        """
        from modules.photo.controller import Controller as PhotoController
        from modules.photo.models import Photo
        results = {
            "count": 0,
            "errors": []
        }
        for photo_obj in Photo.objects():
            results['count'] += 1
            try:
                outfile = os.path.join(app.config['UPLOAD_FOLDER'], photo_obj.file_name)
                PhotoController.save_image_by_ratio(outfile, 's')
                PhotoController.save_image_by_ratio(outfile, 'm')
            except Exception as e:
                app.logger.error("*** run_photo_resize_job occurred an exception")
                app.logger.excetion(e)
                results['errors'].append({'index': results['count'], 'mongo_id': str(photo_obj.id), 'error': e.args})
        return results, 200

    def update_action_prices(self):
        from modules.stock.models import Stock
        from modules.stock_action.models import StockAction, EnumActionTypes
        totals = dict(stok=0, action=0)
        for stok in Stock.objects(buying_price__gt=0).only('list_price', 'buying_price', 'id'):
            totals['stok'] += 1
            for action in StockAction.objects(_key_stock=stok.id):
                totals['action'] += 1
                if action.action_type == EnumActionTypes.GIRIS.value:
                    action.unit_price = stok.buying_price
                elif action.action_type == EnumActionTypes.CIKIS.value and stok.list_price > 0:
                    action.unit_price = stok.list_price
                action.save()
        return totals, 200

    def recalculate_stocks(self):
        from modules.stock.models import Stock
        from modules.stock_action.triggers import StockActionTrigger
        filter_args = json_util.loads(request.args.get('filter_args', '{}'))
        totals = dict(stok=0)
        for stok in Stock.objects(**filter_args):
            totals['stok'] += 1
            StockActionTrigger.update_stock_unit_price(stock_document=stok)
        return totals, 200
