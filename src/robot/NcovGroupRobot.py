import json
import re
import requests
from src.util.constant import USER_FOCUS_GROUP
from urllib import parse

from src.util.log import LogSupport

ls = LogSupport()

def check_whether_identify(text):
    return re.match('^鉴别.+', text) != None

def check_whether_unidentify(text):
    return re.match('^取消鉴别.+', text) != None

def add_identify_group(conn, itchat, group):
    group_name = group.repace("鉴别", '')
    target_chatroom = itchat.search_chatrooms(group_name)
    succ = []
    failed = []
    if len(target_chatroom) > 0:
        chatroom_name = target_chatroom[0]['UserName']
        conn.sadd(USER_FOCUS_GROUP, chatroom_name)
        succ.append(chatroom_name)
    else:
        failed.append(group_name)
    return succ, failed

def cancel_identify_group(conn, itchat, group):
    group_name = group.repace("取消鉴别", '')
    target_chatroom = itchat.search_chatrooms(group_name)
    succ = []
    failed = []
    if len(target_chatroom) > 0:
        chatroom_name = target_chatroom[0]['UserName']
        conn.srem(USER_FOCUS_GROUP, group_name)
        succ.append(chatroom_name)
    else:
        failed.append(group_name)
    return succ, failed

def get_headers():
    return {
        'host': 'vp.fact.qq.com',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'referer': 'https://vp.fact.qq.com/home?state=2'
    }

def get_identify_url(title):
    url = 'https://vp.fact.qq.com/searchresult?'
    params = {
        'title': title,
        'num': 0
    }
    return url + parse.urlencode(params)

def identify_news(text_list, itchat, group_name):
    req = requests.Session()
    for text in text_list:
        res = req.get(url=get_identify_url(text), headers=get_headers())
        if res.status_code != 200:
            ls.logging.error("查询较真平台出错，状态码：{}".format(res.status_code))
        content = res.content.decode("utf-8")
        if content:
            content = json.loads(content)
        else:
            continue
        if content['total'] == 0:
            continue
        elif content['_source']['result'] != '真-确实如此':
            source = content['content']['_source']
            reply = parse_identify_res(text, source)
            # 发送消息
            itchat.send(reply, group_name)
            break


def parse_identify_res(text, source):
    reply_text = '这个{}是{}，真实情况是: {}。你可以点这里看详情'.format(text[0:15], source['result'], source['abstract'], source['oriurl'])
    return reply_text

