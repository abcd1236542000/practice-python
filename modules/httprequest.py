import requests
from requests.cookies import RequestsCookieJar


class httpRequest():
    def doRequest(self, method="get", url="", headers={}, params={}, files={}, data={}, json={}):
        with requests.request(method, url, headers=headers, params=params, files=files, data=data, json=json) as response:
            response.encoding = 'utf-8'
            # response.headers = headers
            # data = response.text
        # return data
        return response

    # def parseJson(self, json_str=""):
    #     try:
    #         import json
    #         data = json.loads(json_str)
    #         return data
    #     except Exception:
    #         # print(traceback.format_exc())
    #         return None
