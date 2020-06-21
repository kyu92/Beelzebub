import requests
import json
import uuid
import time
import datetime
from threading import Timer
from threading import Thread


uid = str(uuid.uuid4())
submit_flag = False
today = datetime.datetime.date(datetime.datetime.now())


def do_submit(circulate: bool):
    login_data = {
        "jsonrpc": "2.0",
        "method": "/v2/login/login",
        "id": 1,
        "params": [account_info['xh'], account_info['xh'], False]}
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

        if circulate:
            confirm = 'y'
        else:
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


def cyc_do(submit_hour: int, submit_minute: int):
    global submit_flag
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    if now_hour == submit_hour and now_minute > submit_minute and submit_flag and 8 < now_hour < 22:
        do_submit(True)
        submit_flag = False
        print(f"当前时间{now}, 开始执行任务")
    elif 8 < submit_hour < now_hour < 22 and submit_flag:
        do_submit(True)
        submit_flag = False
        print(f"当前时间{now}, 开始执行任务")
    else:
        print(f"当前时间{now}, 未到指定时间")
    Timer(60*60*2, lambda: cyc_do(submit_hour, submit_minute)).start()


def reset_flag(submit_hour: int, submit_minute: int):
    global submit_flag, today
    while True:
        now = datetime.datetime.now()
        if now.day - today.day == 1:
            print("日期更新，清除已提交flag")
            submit_flag = True
            today = now
        elif now.day == today.day and (now.hour < submit_hour or (now.hour == submit_hour and now.minute < submit_minute)):
            print("当天时间未到指定提交时间，清除flag")
            submit_flag = True
        time.sleep(60 * 60 * 12)


if __name__ == '__main__':
    with open("resources/data.json", "r", encoding="utf-8") as f:
        account_info = json.load(f)
        circulate = account_info['circulate']
        if circulate:
            submit_time = account_info['submit_on'].split(':')
            hour = int(submit_time[0])
            minute = int(submit_time[1])
            if hour >= 24 or minute >= 60:
                raise Exception("时间填写错误")
            elif not 8 < hour < 22:
                raise Exception("不在可申报时间段")
            else:
                print("开始执行循环任务:")
                cyc_do(hour, minute)
                reset = Thread(target=reset_flag, args=(hour, minute))
                reset.setDaemon(True)
                reset.setName("Thread-Reset_Flag")
                reset.start()
                reset.join()
        else:
            do_submit(circulate)
            input("按任意键继续...")
