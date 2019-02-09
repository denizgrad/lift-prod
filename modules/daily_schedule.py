"""
    created_at: 12/01/2018
    craeted_by: H.BUDAK
    Daily schudule registerer fires every day at 05:30 AM
    You can easily register your function or classmethods with "register_methods_to_daily_job" function
    Example:
        # Register function without class
        register_methods_to_daily_job(func_name)
        # Register class.function
        register_methods_to_daily_job("func_name", class)
"""

from resources import app, SCHEDULE_CTRL

daily_job_list = []


def register_methods_to_daily_job(func, cls=False):
    """
    :param func: string or function | if it's a class method should be string otherways should be function
    :param cls: Class or False | default False
    """
    app.logger.debug("*** register_methods_to_daily_job function fired")
    if cls is False and callable(func) is False:
        app.logger.warning("*** register_methods_to_daily_job first parameter type must be callable "
                           "when second parameter not specified")
    elif cls is not False and isinstance(func, str) is False:
        app.logger.warning("*** register_methods_to_daily_job first parameter type must be String "
                           "when second parameter specified")
    else:
        daily_job_list.append([func, cls])
        app.logger.debug("*** new jobs on daily_job_list {}".format(str(daily_job_list)))


def daily_schedule_job():
    print("*** daily_schedule_job starts")
    try:
        with app.app_context():
            print("*** daily_schedule_job running in app context")
            print("*** app: {}".format(app))
            # app_context altında `request` kullanılacaksa local olarak import edilmelidir
            #  Working outside of request context.
            from flask import request
            app.logger.warning('*** [Schedule Job Fired] daily_schedule_job job fired. Registed daily job count: {}'
                               .format(len(daily_job_list)))
            if len(daily_job_list) > 0:
                for job in daily_job_list:
                    if job[1] is not False and isinstance(job[1], type):
                        try:
                            job[1]().__getattribute__(job[0])()
                        except AttributeError as e:
                            app.logger.error("*** {} has no attribute as {}\n*ERROR: {}".format(job[1], job[0], e))
                        except TypeError as e:
                            app.logger.error("*** {} is not callable\n*ERROR:{}".format(job[0], e))
                        except Exception as e:
                            app.logger.error("*** daily Schedule occurred an exception method: {}\n*ERROR:{}"
                                             .format(job[0], e))
                    else:
                        if callable(job[0]):
                            try:
                                job[0]()
                            except Exception as e:
                                app.logger.error("*** daily Schedule occurred an exception method: {}\n*ERROR: {}"
                                                 .format(job[0], e))
    except Exception as e:
        print("*** daily_schedule_job occurred an exception without start: {}".format([e, e.with_traceback]))
    print("*** daily_schedule_job done")


def register_daily_schedule():
    # Register daily currency request on schedule jobs
    try:
        app.logger.warning("*** daily_schedule_job registering with list of jobs {}".format(daily_job_list))
        SCHEDULE_CTRL.scheduler.add_job(
            daily_schedule_job,
            'cron',
            hour=5,
            minute=30,
            id="daily_schedule_at_05:30",
            name="Daily Schedule fires on every day at 05:30 AM",
            replace_existing=True)
    except Exception as e:
        app.logger.error("*** [Schedule register failed] schedule_xml_parser_job")
        app.logger.exception(e)
