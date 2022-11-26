# b3ack
B3 Tracker - Keep track of Quotations

Aplicação criada com o intuito de facilitar que investidores acompanhem cotações de empresas na B3.

Permite que inestidores pesquisem por cotações monitoradas pela B3, e vejam suas informações.
A partir disto, pode começar a monitorar esta cotação, determinando o intervalo em que deve-se
capturar os dados, e determinando valores máximos e mínimo que, ao atingidos, enviam um e-mail
para este investidor, recomendando a compra/venda.

## Setup
Criar .env com as seguintes variáveis:
```
NOREPLY_EMAIL=noply@b3ack.com (colocar o email que enviará os avisos)
EMAIL_PASS=(senha do email)
```

## Requirements
- celery
- redis
- django-environ
- django-celery
