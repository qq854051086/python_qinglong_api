'''
python操作青龙面板接口的封装
'''
import requests
import json


class QingLong():
    def __init__(self, ql_config):
        json_config = json.loads(ql_config)

        self.host = f"http://{json_config['host']}"
        self.client_id = json_config['ClientID']
        self.client_secret = json_config['ClientSecret']
        self.token = None
        self.task_id = []

        self.header = {
            'Host': f'{json_config["host"]}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
        }

    def run(self):
        # 获取token，启动任务
        if not self.get_qinglong_token():
            print("获取token失败")
            return False

        if not self.get_task_list():
            print("获取任务id失败")
            return False

        if not self.run_task():
            print("执行任务失败")
            return False

        return True

    def get_qinglong_token(self):
        if not self.host and not self.client_id and not self.client_secret:
            print("参数无效")
            return False

        url = self.host + "/open/auth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = self.request_get_method(url, data)
        if response["code"] == 200:
            print("用户认证成功", response)
            self.token = response["data"]["token"]
            return True
        else:
            print(response)
            print("认证失败,退出")
            return False

    def get_task_list(self):
        '''获取任务列表，并筛选出指定的名称任务id'''
        url = f"{self.host}/open/crons"
        response = self.request_get_method(url=url)
        if response["code"] == 200:
            for task in response["data"]:
                print(f"任务名：{task['name']}，任务ID：{task['id']}(运行任务需要发送任务id)")
                # self.task_id.append(task['id'])    #将所有任务的id留存，等于运行所有任务
                return True
        return False

    def run_task(self):
        '''
        运行任务
        :return:
        '''
        url = f"{self.host}/open/crons/run"
        response = self.request_put_method(url=url, data=self.task_id)
        print(response)
        if response["code"] == 200:
            return True
        return False

    def request_get_method(self, url, params=None):
        '''
        青龙的get API
        :param url:
        :param params:
        :return:
        '''
        if self.token:
            self.header.update({"Authorization": f"Bearer {self.token}"})
        response = requests.get(url=url, params=params, headers=self.header, timeout=3)
        response_json = response.json()
        # print("request_get_method青龙响应：", response_json)
        return response_json

    def request_post_method(self, url, data=None):
        '''
        青龙的post API
        :param url:
        :param data:
        :return:
        '''
        if self.token:
            self.header.update({"Authorization": f"Bearer {self.token}"})
        response = requests.post(url=url, json=data, headers=self.header, timeout=3)
        response_json = response.json()
        # print("request_post_method青龙响应：", response_json)
        return response_json

    def request_delete_method(self, url, data=None):
        '''
        青龙的delete API
        :param url:
        :param data:
        :return:
        '''
        if self.token:
            self.header.update({"Authorization": f"Bearer {self.token}"})
        response = requests.delete(url=url, json=data, headers=self.header, timeout=3)
        response_json = response.json()
        # print("request_delete_method.青龙响应：", response_json)
        return response_json

    def request_put_method(self, url, data=None):
        '''
        青龙的 put API
        :param url:
        :param data:
        :return:
        '''
        if self.token:
            self.header.update({"Authorization": f"Bearer {self.token}"})
        response = requests.put(url=url, json=data, headers=self.header, timeout=3)
        response_json = response.json()
        # print("request_delete_method.青龙响应：", response_json)
        return response_json


if __name__ == "__main__":
    config = '{"host":"192.168.0.2:5700","ClientID":"v********qZ_s","ClientSecret":"Ilh**********h"}'
    QingLong(config).run()
