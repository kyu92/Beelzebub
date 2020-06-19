import requests
import json
import uuid
import time

uid = str(uuid.uuid4())

with open("resources/data.json", "r", encoding="utf-8") as f:
    account_info = json.load(f)

login_data = {
    "jsonrpc": "2.0",
    "method": "/v2/login/login",
    "id": 1,
    "params": [account_info['xh'],account_info['xh'],False]}
header = account_info['headers']
session = requests.session()
response = session.post("https://once.tzvcst.edu.cn/mobile/rpc?p=/v2/login/login", json=login_data, headers=header)
result = json.loads(response.text)  # type: dict
if 'error' not in result.keys():
    info = result['result']
    print(f'''
    确认用户信息：
        姓名：{info['display_name']}
        学号：{info['name']}
        身份证号：{info['sfzh']}
        机构: {info['department']['name_path']}
    ''')
    confirm = input("请核对以上信息，并确认信息是否正确(Y/N): ")
    if confirm.lower() == 'y':
        print("确认身份，开始提交表单")
        form_data = {
            "jsonrpc": "2.0",
            "method": "/v2/workorder/action/executeWithValidate",
            "id": 1,
            "params": [
                "a0e8db60-9e6e-11ea-981e-d385212f6fb8",
                [
                    {
                        "id": uid,
                        "type": "91e6efae-894b-11ea-b19d-97bc1248cc63",
                        "node": "9f8fb3d8-9e6e-11ea-bcb4-37881e21d6ac"
                    },
                    {
                        "id": uid,
                        "type": "91e6efae-894b-11ea-b19d-97bc1248cc63",
                        "source": "wechat",
                        "apply_user": info['id'],
                        "apply_department": info['department']['id'],
                        "xm": info['display_name'],
                        "xh": info['name'],
                        "banji": info['department']['id'],
                        "xy": info['department']['name_path'].split('.')[2],
                        "lxdh": account_info['mobile'],
                        "rq": int(round(time.time() * 1000)),
                        "jrsfzx": "zx",
                        "jrszs": None,
                        "zctwfw": "yx",
                        "zwtwfw": "yx",
                        "jrsfqj": "fou",
                        "jrywrxzz": "wu",
                        "jrsf": "fou",
                        "mqtzjkmys": "lvs"
                    },
                    {
                        "service_catalog": "d31f2d28-8956-11ea-9264-8fc0de5ccc83"
                    }
                ],
                [
                    "a9f2ea09-894b-11ea-ba5f-af12318e09ed"
                ]
            ]
        }
        response = session.post("https://once.tzvcst.edu.cn/mobile/rpc?p=/v2/workorder/action/executeWithValidate",
                                json=form_data, headers=header)
        print(response.text)
    else:
        print("未核实身份，退出程序")
else:
    print("未找到用户信息,请确认学号是否正确")
input("任意键继续...")
