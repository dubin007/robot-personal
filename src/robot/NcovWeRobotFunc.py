import re
import jieba
from src.util.constant import BASE_DIR, ALL_AREA_KEY

jieba.load_userdict(BASE_DIR + "all_area.txt")
def check_whether_register(text):
    return re.match('^订阅.+', text) != None

def user_subscribe(conn, user, area):
    """
    接收用户订阅
    :param conn: redis 连接
    :param user: 用户名
    :param area: 发送订阅的文字，如订阅湖北省
    :return:
    """
    all_area = set(conn.smembers(ALL_AREA_KEY))
    jieba.add_word(list(all_area))
    # 去掉订阅两字
    area = area.replace("订阅", '')
    area_list = jieba.cut(area)
    succ_subscribe = []
    failed_subscribe = []
    tails = ['省', '市', '区', '县','州','自治区', '自治州', '']
    for ar in area_list:
        flag = False
        for tail in tails:
            if ar + tail in all_area:
                conn.rpush(ar + tail, user)
                succ_subscribe.append(ar + tail)
                flag =True
                break

        if not flag:
            failed_subscribe.append(ar)

    return succ_subscribe, failed_subscribe
