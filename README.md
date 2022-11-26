# b3ack
B3 Tracker - Keep track of Quotations

Aplicação criada com o intuito de facilitar que investidores acompanhem cotações de empresas na B3.

# Setup
1. Criar .env com as seguintes variáveis:
NOREPLY_EMAIL=noply@b3ack.com (colocar o email que enviará os avisos)
EMAIL_PASS=(senha do email)

# Requirements
- celery
- redis
- django-environ
- django-celery