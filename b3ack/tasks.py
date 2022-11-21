from b3ack.utils.bcolors import bcolors
from b3ack.utils.b3api import B3api
from celery import shared_task
from b3ack.models import Company
import datetime

@shared_task()
def fetch_stock_task(company_code: str):
    api = B3api()
    print(bcolors.OKCYAN + f"> Fetching data for {company_code}..." + bcolors.ENDC)

    stock_code = api.data[company_code]['cd_acao'].split(',')[0]
    data = api.get_quotes(cod=company_code)

    print(bcolors.OKGREEN + f"> Got data for {company_code}!" + bcolors.ENDC)

    
    if data is None: 
        pass
    else:
        stock_data = data[stock_code]
        print(stock_data)
        c = Company.objects.get(code=company_code)

        print(f"Company = {c}")

        dt = datetime.datetime.now()
        dt_str = str(dt.strftime("%d/%m, %H:%M"))

        if c.abr is None:
            c.abr = stock_data['vl_abertura']
            c.max = stock_data['vl_maximo']
            c.min = stock_data['vl_minimo']
            c.fch = stock_data['vl_fechamento']
            c.capture_dt = dt_str


        else:
            c.abr.append(stock_data['vl_abertura'])
            c.max.append(stock_data['vl_maximo'])
            c.min.append(stock_data['vl_minimo'])
            c.fch.append(stock_data['vl_fechamento'])
            c.capture_dt.append(dt_str)

        c.save()