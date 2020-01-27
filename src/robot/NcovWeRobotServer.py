import json
import time
import itchat
from itchat.content import *
from src.robot.NcovWeRobotFunc import *
from src.util.constant import INFO_TAIL, SHOULD_UPDATE, UPDATE_CITY, UPDATE_NCOV_INFO, SHORT_TIME_SPLIT
from src.util.redis_config import connect_redis
import jieba
import multiprocessing
from src.spider.SpiderServer import start_tx_spider

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    if msg['FromUserName'] == itchat.originInstance.storageClass.userName:
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
            itchat.send(get_ncvo_info_with_city(conn, succ), toUserName=msg.user.UserName)
            area = succ[0]
            itchat.send(INFO_TAIL.format(area, area), toUserName=msg.user.UserName)
    elif check_whether_unregist(msg.text):
        succ, failed = user_unsubscribe_multi(conn, msg.user.UserName, msg.text, jieba)
        succ_text = ''
        if len(succ) > 0:
            succ_text = '成功取消{}的疫情信息订阅'.format("，".join(succ))
        failed_text = ''
        if len(failed) > 0:
            failed_text ='取消{}的疫情信息订阅失败，您好像没有订阅该地区信息或者地区名称错误'.format("，".join(failed))
        ls.logging.info('用户%s: %s %s' % (msg.user.UserName, succ_text, failed_text))
        itchat.send('%s %s' % (succ_text, failed_text), toUserName=msg.user.UserName)

def init_jieba():
    all_area = set(conn.smembers(ALL_AREA_KEY))
    if len(all_area) == 0:
        ls.logging.error("尚无地区信息")

    for words in all_area:
        jieba.add_word(words)
    return jieba

def do_ncov_update(conn, itchat, debug=True):
    ls.logging.info("thread do ncov update info start success-----")
    try:
        while True:
            should_update = conn.get(SHOULD_UPDATE)
            if should_update == '1':
                update_city = conn.get(UPDATE_CITY)
                conn.set(SHOULD_UPDATE, 0)
                if not update_city:
                    ls.logging.warning("-No update city info")
                    continue
                update_city = json.loads(update_city)
                for city in update_city:
                    push_info = UPDATE_NCOV_INFO.format(city['city'], city['n_confirm'], city['confirm'], city['dead'], city['heal'])
                    subscribe_user = conn.smembers(city['city'])
                    for user in subscribe_user:
                        itchat.send(push_info, toUserName=user)
            if debug:
                break
            # 暂停几分钟
            time.sleep(SHORT_TIME_SPLIT)
    except BaseException as e:
        ls.logging.error("Error in check ncov update-----")
        ls.logging.exception(e)


def start_server():
    itchat.auto_login(False)
    p1 = multiprocessing.Process(target=start_tx_spider)
    p1.start()
    p2 = multiprocessing.Process(target=do_ncov_update, args=[conn, itchat, False])
    p2.start()
    itchat.send('Hello, 自动机器人又上线啦', toUserName='filehelper')
    itchat.run(True)

if __name__ == '__main__':
    conn = connect_redis()
    jieba = init_jieba()
    start_server()

