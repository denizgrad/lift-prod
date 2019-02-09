from flask import Blueprint

"""
 *** Blueprint registers for "Photo" module ***
"""
photo_views = Blueprint('photo',
                       __name__,
                       template_folder="templates",
                       static_folder="static")








