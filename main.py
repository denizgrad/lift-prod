# coding=utf-8

from resources import app, SCHEDULE_CTRL, ScheduleController
from modules.daily_schedule import register_daily_schedule
from modules import signals


@app.route("/", endpoint="home")
def homepage(name=None):
    return ""

from modules.user import routers
from modules.user.auth import routers
from modules.organization import routers
from modules.currency import routers
from modules.account import routers
from modules.contact import routers
from modules.contact.contactItem import routers
from modules.permission import routers
from modules.project import routers
from modules.quote import routers
from modules.analyzes.cabin import routers
from modules.analyzes.cabin.cabintypes import routers
from modules.analyzes.console import routers
from modules.analyzes.console.consoletype import routers
from modules.analyzes.controlPanel import routers
from modules.analyzes.controlPanel.panelsize import routers
from modules.analyzes.controlPanel.controlpanelextra import routers
from modules.analyzes.controlPanel.controlpanelbuttontype import routers
from modules.analyzes.rail import routers
from modules.analyzes.rail.railsize import routers
from modules.analyzes.part import routers
from modules.analyzes.part.parttype import routers
from modules.analyzes.machineEngine.capacity import routers
from modules.analyzes.machineEngine.enginespeed import routers
from modules.analyzes.machineEngine.enginetype import routers
from modules.analyzes.machineEngine.roomtype import routers
from modules.analyzes.machineEngine.volume import routers
from modules.analyzes.machineEngine import routers
from modules.analyzes.door.doorsize import routers
from modules.analyzes.door.doortype import routers
from modules.analyzes.door.paneltype import routers
from modules.analyzes.door import routers
from modules.brand import routers
# ======== Rest Endpoints ========
from modules import rest_endpoints
# ======== Admin Route ===========
from admin_route import routers

if isinstance(SCHEDULE_CTRL, ScheduleController) and SCHEDULE_CTRL.scheduler.running is not True:
    register_daily_schedule()
    app.logger.warning("*** SCHEDULE_CTRL.run_schedules fired")
    SCHEDULE_CTRL.run_schedules()
    app.logger.warning("*** list of jobs: {}".format(str(SCHEDULE_CTRL.scheduler.get_jobs())))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=app.config.get('APP_DEBUG', True))

