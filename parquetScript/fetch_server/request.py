import requests
import json

class FetchUrl:
    """call to api_url and return calssification array"""
    def __init__(self, api_url):
        self.api_url = api_url
        self.api_header = {"Content-Type": "application/json"}

    def fetchApi(self, params):
        try:
            responce = requests.post(self.api_url, data=json.dumps(params), headers=self.api_header)
            batch_result = responce.json()['classification']
        except Exception as e:
            print(e)
        else:
            return batch_result

