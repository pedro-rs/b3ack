"""Tasks consumed by Celery in the background.
"""

from b3ack.utils.bcolors import bcolors
from b3ack.utils.b3api import B3api
from b3ack.utils.email import Email
from celery import shared_task
from b3ack.models import CompanyTracker
import datetime

@shared_task()
def fetch_stock_task(company_code: str, tracker_id: int):
    # Track data for the company
    api = B3api()
    print(bcolors.OKCYAN + f"> Fetching data for {company_code}..." + bcolors.ENDC)

    # stock_code = api.data[company_code]['cd_acao'].split(',')[0]
    data = api.get_quotes(code=company_code)

    if data is None: 
        print(bcolors.FAIL + f"> Error fetching data for {company_code}" + bcolors.ENDC)

    else:
        print(bcolors.OKGREEN + f"> Got data for {company_code}!" + bcolors.ENDC)
        stock_data = list(data.values())[0]
        ct = CompanyTracker.objects.get(id=tracker_id)

        dt = datetime.datetime.now()
        dt_str = str(dt.strftime("%d/%m, %H:%M"))

        # Register data in database model
        if ct.abr is None:
            ct.abr = [stock_data['vl_abertura']]
            ct.max = [stock_data['vl_maximo']]
            ct.min = [stock_data['vl_minimo']]
            ct.fch = [stock_data['vl_fechamento']]
            ct.capture_dt = [dt_str]

        else:
            ct.abr.append(stock_data['vl_abertura'])
            ct.max.append(stock_data['vl_maximo'])
            ct.min.append(stock_data['vl_minimo'])
            ct.fch.append(stock_data['vl_fechamento'])
            ct.capture_dt.append(dt_str)

        ct.save()

        # If value is above sell line or below buy line, alert user
        if ct.sell_value and stock_data['vl_fechamento'] > ct.sell_value:
            print(f"Sending sell email to {ct.user.email}")
            e = Email()
            e.send(
                ct.user.email, 
                f"Compre cotacoes de {ct.code}!", 
                f"""O tracker do B3ack detectou que o valor das cotacoes de {ct.code}\
                atingiram o valor de R${stock_data['vl_fechamento']}. Como este valor\
                e maior que {ct.sell_value}, configurado por voce, recomendamos\
                a venda desta cotacao!"""
            )

        elif ct.buy_value and stock_data['vl_fechamento'] < ct.buy_value:
            print(f"Sending buy email to {ct.user.email}")
            e = Email()
            e.send(
                ct.user.email, 
                f"Compre cotacoes de {ct.code}!", 
                f"""O tracker do B3ack detectou que o valor das cotacoes de {ct.code}\
                atingiram o valor de R${stock_data['vl_fechamento']}. Como este valor\
                e menor que {ct.buy_value}, configurado por voce, recomendamos\
                a compra desta cotacao!""")
