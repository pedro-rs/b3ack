from threading import Timer
from b3ack.utils.bcolors import bcolors
from b3ack.utils.b3api import B3api
from datetime import datetime
from b3ack.models import CompanyTracker
from b3ack.tasks import fetch_stock_task

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class Tracking():
    def __init__(self):
        """
        Args:
            interval (int): Interval, in seconds, between fetching quotes
            for tracked companies
        """
        print(bcolors.OKGREEN + "Initializing tracker!" + bcolors.ENDC)

    def start_tracking(self, interval: int, company_code: str, tracker_id: int):
        # Initializing API
        RepeatedTimer(interval, self.get_quote, company_code, tracker_id)

    def get_quote(self, company_code: str, tracker_id: int):       
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # Logging
        print(bcolors.OKBLUE + f"*** [{dt_string}] Tracking quotes for {company_code}" + bcolors.ENDC)

        fetch_stock_task.delay(company_code, tracker_id)