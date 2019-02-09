import sys

sys.path.insert(0, '/app/')
sys.path.append('X:/xamppPhp7/htdocs/projects/Python/otoservis')

from main import app as application

application.config['TEMPLATES_AUTO_RELOAD'] = True
