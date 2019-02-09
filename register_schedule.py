from apscheduler.schedulers.background import BackgroundScheduler
import atexit
# from apscheduler.triggers.interval import IntervalTrigger


class ScheduleController:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        # self.scheduler.add_job()

    def run_schedules(self):
        try:
            self.scheduler.start()
            # Shut down the scheduler when exiting the app
            atexit.register(lambda: self.scheduler.shutdown())
        except Exception as e:
            print("*** ScheduleController.run_schedules occurred an exception: {}".format([e, e.with_traceback]))

    def get_pending_jobs(self, job_id=None):
        """
        Get list of jobs or get job by job_id
        :param job_id: string | optional if it's not none returns job which equals job_id
        :returns: List or Dict
        """
        try:
            if job_id is not None:
                return self.scheduler.get_job(job_id)
            else:
                return self.scheduler.get_jobs()
        except Exception as e:
            pass

    def register_schedule(self, callback, trigger_timer, job_id, name=None):
        """
        Void method
        Schedule registerer hook
        :param callback: function
        :param trigger_timer: the alias name of the trigger (e.g. ``date``, ``interval`` or ``cron``)
        :param job_id: string | Schedule job id
        :param name: string | optional name of job
        """
        if callable(callback) is False:
            return False
        else:
            self.scheduler.add_job(
                func=callback,
                trigger=trigger_timer,
                id=job_id,
                name=name if name is not None else str(job_id)+" Schedule registered without name",
                replace_existing=True)
