import threading
import time

import schedule


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    print(f"Time until next job: {schedule.idle_seconds()} seconds")

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                print("Schedule Active!")
                schedule.run_pending()
                time.sleep(interval)
            print("Schedlue deactivated!")

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run
