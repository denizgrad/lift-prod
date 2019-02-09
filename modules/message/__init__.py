from flask import Blueprint
message_views = Blueprint('message',
                       __name__,
                       template_folder="templates",
                       static_folder="static")