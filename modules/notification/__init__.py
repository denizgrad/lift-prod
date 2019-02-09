from flask import Blueprint
notification_views = Blueprint('notification',
                       __name__,
                       template_folder="templates",
                       static_folder="static")