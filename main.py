import requests
from receive import rev_msg
import socket


# 发送消息函数
def send_msg(resp_dict):
    global payload
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect((ip, 5700))

    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息

    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    # if msg_type == 'group':
    #     payload = "GET /send_group_msg?group_id=" + str(
    #         number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    # el
    if msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


# 控制整个机器人运行
def main02():
    while True:
        try:
            rev = rev_msg()
            print(rev)
            if rev == None:
                continue
        except:
            continue

        if rev["post_type"] == "message":
            message = rev['raw_message']
            data = {
                "appid": "f09975adb64fa500659f57e36a9b1fcc",
                "userid": "Pwa8iOCo",
                "spoken": message,
            }
            url = 'https://api.ownthink.com/bot'
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url=url, data=data, headers=headers)
            print(response.status_code)
            response.encoding = 'utf-8'
            result = response.json()
            answer = result['data']['info']['text']
            if rev['message_type'] == 'private':  #
                qq = rev['sender']['user_id']
                send_msg({'msg_type': 'private', 'number': qq, 'msg': answer})
            elif rev['message_type'] == 'group':
                qq01 = rev['group_id']
                send_msg({'msg_type': 'group', 'number': qq01, 'msg': answer})


if __name__ == '__main__':
    main02()