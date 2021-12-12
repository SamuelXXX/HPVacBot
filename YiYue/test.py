# -*- encoding:utf-8 -*-

import requests
import copy
import json
import time



class YiyueBot(object):
    URL="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx"

    BASE_HEADERS={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "Referer": "https://servicewechat.com/wx2c7f0f3c30d99445/91/page-frame.html",
        "content-type": "application/json, text/plain, */*",
    }

    def http_get(self, params=None, additional_headers=None):
        headers=copy.deepcopy(self.BASE_HEADERS)
        if additional_headers is not None:
            headers.update(additional_headers)
        try:
            response = requests.get(self.URL, params, headers=headers)
            response.raise_for_status()
        except Exception as err:
            error_response = f'URL:{self.URL} ERROR:{err}'
            print(error_response)
        else:
            res_json = response.json()
            _suc_msg = f'{self.URL}\n{"-" * 5 + "Request" + "-" * 5}\n{params}\n{"-" * 5 + "Response" + "-" * 5}\n{res_json}\nuseTime:{response.elapsed.total_seconds()}S\n'
            # print(_suc_msg)
            return res_json
    
    def query_vaccines(self):
        params={
            "act":"CustomerList",
            "city":'["四川省","成都市",""]',
            "id":"0",
            "cityCode":"510100",
            "product":"1",
        }
        return self.http_get(params=params)
    
    def query_vaccine_detail(self, vaccine_id):
        params={
            "act":"CustomerProduct",
            "id":"%s"%vaccine_id,
        }
        return self.http_get(params=params)


if __name__=="__main__":
    bot=YiyueBot()
    data=bot.query_vaccines()

    for item in data["list"]:
        print(item["id"])
        vac_result=bot.query_vaccine_detail(item["id"])
        if vac_result and len(vac_result["list"])!=0:
            # print(vac_result)
            for vac in vac_result["list"]:
                if vac["date"]=="暂无":
                    continue

                if vac["text"]!="九价人乳头瘤病毒疫苗":
                    continue
                print(vac["date"])
                print("%s:%s"%(vac_result["addr"],vac["date"]))
        
        time.sleep(0.5)
    
    bot.query_vaccine_detail(2560)