from threading import Timer
from b3ack.utils.bcolors import bcolors
from b3ack.utils.b3api import B3api
from datetime import datetime
from b3ack.models import Company
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
    def __init__(self, interval: int):
        """
        Args:
            interval (int): Interval, in seconds, between fetching quotes
            for tracked companies
        """
        self.interval = interval
        print(bcolors.OKGREEN + "Initializing tracker!" + bcolors.ENDC)

    def start_tracking(self):
        # Initializing API
        self.api = B3api()

        self.get_quote()
        RepeatedTimer(self.interval, self.get_quote)

    def get_quote(self):       
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        print(bcolors.OKBLUE + f"*** [{dt_string}] Tracking quotes!" + bcolors.ENDC)

        tracked_companies = Company.objects.all()

        if len(tracked_companies) == 0:
            print(bcolors.FAIL + "No companies to track currently." + bcolors.ENDC)
            return

        # TODO: This would ideally be done in parallel!
        for company in tracked_companies:
            # self.fetch_stock(company.code)
            fetch_stock_task.delay(company.code)
            print("Here!")

    # def fetch_stock(self, company_code: str):
    #     print(bcolors.OKCYAN + f"Fetching data for {company_code}..." + bcolors.ENDC)

    #     stock_code = self.api.data[company_code]['cd_acao'].split(',')[0]
    #     data = self.api.get_quotes(cod=company_code)

    #     print(bcolors.OKGREEN + f"Got data for {company_code}!" + bcolors.ENDC)
    #     if data is not None: print(data[stock_code])