"""Abstraction of calls to the B3 API for companies/quotes. 
"""

from typing import Optional
import requests
import json 

class B3api:
    def __init__(self):
        # Initialize main dictionary with companies and information
        res = requests.get('https://api-cotacao-b3.labdo.it/api/empresa/group/segmento_b3')
        response = json.loads(res.text)['']

        # Using company's codes as keys for easier access in the future
        self.data = dict()
        for i in response:
            self.data[i['cd_acao_rdz']] = i

    def get_quotes(self, id: Optional[int]=None, code: Optional[str]=None) -> Optional[dict]:
        """Get quote prices for a given company.

        Args:
            id (int, optional): Company ID in the API. Defaults to None.
            code (str, optional): Company's code. Defaults to None.

        Only one of the two is necessary.

        Returns:
            Optional[dict]: dictionary containing quote prices for the company,
            where keys are the quote's code.
        """
        if code is not None:
            id = self.data[code]['id']

        if id is not None:
            endpoint = f"https://api-cotacao-b3.labdo.it/api/empresa/{id}/cotacoes"
            res = requests.get(endpoint)
            response = json.loads(res.text)

            data = dict()
            for i in response:
                data[i['cd_acao']] = i

            return data

        return None