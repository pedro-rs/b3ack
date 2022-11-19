from typing import Optional
import requests
import json 

class B3api:
    def __init__(self):
        res = requests.get('https://api-cotacao-b3.labdo.it/api/empresa/group/segmento_b3')
        response = json.loads(res.text)['']

        # Using business' codes as dict keys
        self.data = dict()
        for i in response:
            self.data[i['cd_acao_rdz']] = i

    def get_quotes(self, id=None, cod=None) -> Optional[dict]:
        if cod is not None:
            id = self.data[cod]['id']

        if id is not None:
            endpoint = f"https://api-cotacao-b3.labdo.it/api/empresa/{id}/cotacoes"
            res = requests.get(endpoint)
            response = json.loads(res.text)

            return response

        return None