# B3 Tracker - Keep track of Quotations

Aplicação criada com o intuito de facilitar que investidores acompanhem cotações de empresas na B3.

Permite que inestidores pesquisem por cotações monitoradas pela B3, e vejam suas informações.
A partir disto, pode começar a monitorar esta cotação, determinando o intervalo em que deve-se
capturar os dados, e determinando valores máximos e mínimo que, ao atingidos, enviam um e-mail
para este investidor, recomendando a compra/venda.
<br></br>
## **Setup**
**Criar .env com as seguintes variáveis:**
```
NOREPLY_EMAIL=noply@b3ack.com (colocar o email que enviará os avisos)
EMAIL_PASS=(senha do email)
```

**Inicializar redis e celery junto ao servidor:**
```
$ redis-server
$ python3 -m celery -A b3 worker -l info
$ python3 manage.py runserver
```
