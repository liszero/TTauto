import requests,json
from commons.decorator_log import logs

class base_request():
    def __init__(self,method,host,params,headers,datatype,body):
        self.method = method
        self.host = host
        self.params = params
        self.headers = headers
        self.type = datatype
        self.body = body

    @logs
    def run_request(self):
        if self.headers != "" and self.headers != None:
            new_headers = eval(self.headers)
        else:
            new_headers = self.headers

        if self.params != "" and self.params != None:
            new_params = eval(self.params)
        else:
            new_params = self.params
        if self.method == "get":
            r = requests.get(url=self.host,headers=new_headers,params=new_params,verify=False)
            r_dict = {}
            r_dict["header"] = r.headers
            r_dict["body"] = r.json()
            r_dict["costtime"] = r.elapsed.total_seconds()
            return r_dict

        elif self.method == "post":
            if self.type != "" and self.type != None:
                new_body = eval(self.body)
                if self.type == "json":
                    payload = json.dumps(new_body)
                else:
                    payload = new_body
            else:
                payload = ""
            r = requests.post(url=self.host,headers=new_headers,params=new_params,data=payload,verify=False)
            r_dict = {}
            r_dict["header"] = eval(str(r.headers))
            r_dict["body"] = r.json()
            r_dict["costtime"] = str(r.elapsed.total_seconds())
            return r_dict
