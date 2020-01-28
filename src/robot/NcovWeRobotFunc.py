import re
from src.util.constant import ALL_AREA_KEY, AREA_TAIL, FIRST_NCOV_INFO, NO_NCOV_INFO, ORDER_KEY, UN_REGIST_PATTERN, \
    UN_REGIST_PATTERN2
from src.util.log import LogSupport
from src.util.redis_config import load_last_info

ls = LogSupport()
def check_whether_register(text):
    return re.match('^订阅.+', text) != None

def user_subscribe(conn, user, area, jieba):
    """
    接收用户订阅
    :param conn: redis 连接
    :param user: 用户名
    :param area: 发送订阅的文字，如订阅湖北省
    :return:
    """
    all_area = set(conn.smembers(ALL_AREA_KEY))
    if len(all_area) == 0:
        ls.logging.error("all area key 为空")
    # 去掉订阅两字
    area = area.replace("订阅", '')
    area_list = jieba.cut(area)
    area_list = list(filter(lambda x: len(x) > 1, area_list))
    succ_subscribe = []
    failed_subscribe = []
    tails = ['省', '市', '区', '县','州','自治区', '自治州', '']

    for ar in area_list:
        ar = re.subn(AREA_TAIL, '', ar)[0]
        if ar == '中国' or ar == '全国':
            conn.sadd('全国', user)
            conn.sadd(ORDER_KEY, '全国')
            succ_subscribe.append('全国')
        else:
            flag = False
            for tail in tails:
                if ar + tail in all_area:
                    # 使该地区的键值唯一，以腾讯新闻中的名称为准，比如湖北省和湖北都使用湖北，而涪陵区和涪陵都使用涪陵区
                    conn.sadd(ar + tail, user)
                    conn.sadd(ORDER_KEY, ar + tail)
                    succ_subscribe.append(ar + tail)
                    flag =True
                    break
            if not flag:
                failed_subscribe.append(ar)
    return succ_subscribe, failed_subscribe

def check_whether_unregist(text):
    return re.match(UN_REGIST_PATTERN, text) != None

def user_unsubscribe_multi(conn, user, area, jieba):
    """
    取消订阅
    :param conn:
    :param user:
    :param area:
    :param jieba:
    :return:
    """
    all_order_area = conn.smembers(ORDER_KEY)
    unsubscribe_list = []
    unsubscribe_list_fail = []
    # 全部取消订阅
    if area.find("全部") != -1 or area.find("全国") != -1:
        for area in all_order_area:
            conn.srem(area, user)
        unsubscribe_list.append("全部")
        return unsubscribe_list, unsubscribe_list_fail
    area = re.subn(UN_REGIST_PATTERN2, '', area)[0]
    area_list = jieba.cut(area)
    for ar in area_list:
        flag = False
        ar = re.subn(AREA_TAIL, '', ar)[0]
        if ar in all_order_area:
            ret = conn.srem(ar, user)
            if ret > 0:
                unsubscribe_list.append(ar)
            else:
                unsubscribe_list_fail.append(ar)
        else:
            # 比如用户订阅时使用的是湘西自治州，取消订阅时使用的湘西，则取消一个个查找
            for order_area in all_order_area:
                if order_area.startswith(ar):
                    flag = True
                    ret = conn.srem(order_area, user)
                    if ret > 0:
                        unsubscribe_list.append(order_area)
                    else:
                        unsubscribe_list_fail.append(order_area)
                    break
            if not flag:
                unsubscribe_list_fail.append(ar)

    return unsubscribe_list, unsubscribe_list_fail

def get_ncvo_info_with_city(conn, citys):
    """
    根据传入的城市列表获取疫情信息
    :param conn: redis连接
    :param citys:
    :return:
    """
    last = load_last_info(conn)
    ncov = []
    for city in citys:
        if city in last:
            info = last[city]
            ncov.append(FIRST_NCOV_INFO.format(info['city'], info['confirm'], info['dead'], info['heal']))
        else:
            ncov.append(NO_NCOV_INFO.format(city))
    return "；".join(ncov)

def restore_we_friend(conn, itchat):

    pass
