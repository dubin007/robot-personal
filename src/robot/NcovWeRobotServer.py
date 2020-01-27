import itchat
from itchat.content import *
from src.robot.NcovWeRobotFunc import *
from src.util.constant import INFO_TAIL
from src.util.redis_config import connect_redis
import jieba

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
        itchat.send(get_ncvo_info_with_city(conn, succ), toUserName=msg.user.UserName)
        itchat.send(INFO_TAIL, toUserName=msg.user.UserName)


def init_jieba():
    all_area = set(conn.smembers(ALL_AREA_KEY))
    if len(all_area) == 0:
        ls.logging.error("尚无地区信息")
        raise BaseException

    for words in all_area:
        jieba.add_word(words)
    return jieba

def start_server():
    itchat.auto_login(True)
    itchat.send('Hello, 自动机器人又上线啦', toUserName='filehelper')
    itchat.run(True)

if __name__ == '__main__':
    conn = connect_redis()
    jieba = init_jieba()
    start_server()

