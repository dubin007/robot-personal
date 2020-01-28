import json
import time
import itchat
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
BASE_PATH = os.path.split(rootPath)[0]
sys.path.append(BASE_PATH)
from itchat.content import *
from src.robot.NcovWeRobotFunc import *
from src.util.constant import INFO_TAIL, INFO_TAIL_ALL, SEND_SPLIT, FOCUS_TAIL
from src.util.redis_config import connect_redis
from src.robot.NcovGroupRobot import *

import jieba
import threading
from src.spider.SpiderServer import start_tx_spider

@itchat.msg_register([TEXT])
def text_reply(msg):
    if msg['FromUserName'] == itchat.originInstance.storageClass.userName and msg['ToUserName'] != 'filehelper':
        return
    if check_whether_register(msg.text):
        succ, failed = user_subscribe(conn, msg.user.UserName, msg.text, jieba)
        succ_text = ''
        if len(succ) > 0:
            succ_text = '成功订阅{}的疫情信息!'.format(",".join(succ))
        failed_text = ''
        if len(failed) > 0:
            failed_text = '订阅{}失败，该地区名称不正确或暂无疫情信息。'.format("，".join(failed))
        # msg.user.send('%s: %s' % (succ_text, failed_text))
        ls.logging.info('用户%s: %s %s' % (msg.user.UserName, succ_text, failed_text))
        itchat.send('%s %s' % (succ_text, failed_text), toUserName=msg.user.UserName)
        if len(succ) > 0:
            time.sleep(SEND_SPLIT)
            itchat.send(get_ncvo_info_with_city(conn, succ), toUserName=msg.user.UserName)
            area = succ[0]
            if area != '全国' and area != '中国':
                time.sleep(SEND_SPLIT)
                itchat.send(INFO_TAIL.format(area, area), toUserName=msg.user.UserName)
            else:
                time.sleep(SEND_SPLIT)
                itchat.send(INFO_TAIL_ALL, toUserName=msg.user.UserName)
    elif check_whether_unregist(msg.text):
        succ, failed = user_unsubscribe_multi(conn, msg.user.UserName, msg.text, jieba)
        succ_text = ''
        if len(succ) > 0:
            succ_text = '成功取消{}的疫情信息订阅'.format("，".join(succ))
        failed_text = ''
        if len(failed) > 0:
            failed_text = '取消{}的疫情信息订阅失败，您好像没有订阅该地区信息或者地区名称错误'.format("，".join(failed))
        ls.logging.info('用户%s: %s %s' % (msg.user.UserName, succ_text, failed_text))
        itchat.send('%s %s' % (succ_text, failed_text), toUserName=msg.user.UserName)

    elif msg['ToUserName'] == 'filehelper' and check_whether_identify(msg.text):
        succ, failed = add_identify_group(conn, itchat, msg.text)
        succ_text =''
        failed_text = ''
        if len(succ) > 0:
            succ_text = '成功关注{}，会自动鉴别该群的疫情谣言'.format("，".join(succ))
        else:
            failed_text = '关注{}失败，请检查该群名称是否正确'.format("，".join(failed))
        ls.logging.info('用户%s: %s %s' % (msg.user.UserName, succ_text, failed_text))
        itchat.send('%s %s' % (succ_text, failed_text), toUserName='filehelper')
        if len(succ) > 0:
            time.sleep(SEND_SPLIT)
            itchat.send(FOCUS_TAIL, toUserName='filehelper')

    elif msg['ToUserName'] == 'filehelper' and check_whether_unidentify(msg.text):
        succ, failed = cancel_identify_group(conn, itchat, msg.text)
        succ_text = ''
        failed_text = ''
        if len(succ) > 0:
            succ_text = '取消鉴别{}成功'.format("，".join(succ))
        else:
            failed_text = '取消鉴别{}失败，请检查该群名称是否正确'.format("，".join(failed))
        ls.logging.info('用户%s: %s %s' % (msg.user.UserName, succ_text, failed_text))
        itchat.send('%s %s' % (succ_text, failed_text), toUserName='filehelper')


@itchat.msg_register([TEXT, NOTE, PICTURE, SHARING, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def text_reply(msg):
    if msg['FromUserName'] == itchat.originInstance.storageClass.userName and msg['ToUserName'] != 'filehelper':
        return
    focus_group = conn.smembers(USER_FOCUS_GROUP)
    if msg['FromUserName'] not in focus_group:
        return

    print(msg.text)
    print(msg)
    taget_chatroom = itchat.search_chatrooms('【TEXT】')
    chatroom_name = taget_chatroom[0]['UserName']
    msg.download(msg.fileName)
    print(taget_chatroom[0])
    print(chatroom_name)

    if chatroom_name in msg['FromUserName']:
        if str(msg['Text']) in ['start']:
            itchat.send('测试成功', msg['FromUserName'])
    if chatroom_name in msg['ToUserName']:
        if str(msg['Text']) in ['start']:
            itchat.send('测试成功', msg['ToUserName'])

def init_jieba():
    all_area = set(conn.smembers(ALL_AREA_KEY))
    if len(all_area) == 0:
        ls.logging.error("尚无地区信息")

    for words in all_area:
        jieba.add_word(words)
    return jieba

def start_server():
    # 在不同的终端上，需要调整CMDQR的值
    itchat.auto_login(True, enableCmdQR=2)
    ls.logging.info("begin to start tx spider")
    p1 = threading.Thread(target=start_tx_spider)
    p1.start()
    ls.logging.info("begin to start ncov update")
    p2 = threading.Thread(target=do_ncov_update, args=[conn, itchat, False])
    p2.start()
    itchat.send('Hello, 自动机器人又上线啦', toUserName='filehelper')
    itchat.run(True)

conn = connect_redis()
jieba = init_jieba()

if __name__ == '__main__':
    start_server()
