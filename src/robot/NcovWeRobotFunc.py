import random
import re
import time

from src.util.constant import ALL_AREA_KEY, AREA_TAIL, FIRST_NCOV_INFO, NO_NCOV_INFO, ORDER_KEY, UN_REGIST_PATTERN, \
    UN_REGIST_PATTERN2, SHOULD_UPDATE, UPDATE_CITY
from src.util.log import LogSupport
from src.util.redis_config import load_last_info
import json

from src.util.util import get_random_tail, get_random_split, get_random_long_time

ls = LogSupport()
def check_whether_register(text):
    return re.match('^订阅.+', text) != None

def user_subscribe(conn, user, area, jieba):
    """
    接收用户订阅
    :param conn: redis 连接
    :param user: 用户名
    :param area: 发送订阅的文字，如订阅湖北省
    :param jieba: jieba分词的对象，从外部传入是为了加载额外的词库
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
    if area.find("全部") != -1:
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
    """
    添加好友，但是微信已经禁止了网页版添加好友的功能
    :param conn:
    :param itchat:
    :return:
    """
    all_order_area = conn.smembers(ORDER_KEY)
    all_users = set()
    for order_area in all_order_area:
        users = itchat.smembers(order_area)
        all_users.union(users)

    for user in all_users:
        itchat.add_friend(userName=user)

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
                    push_info = construct_push_info(city)
                    subscribe_user = conn.smembers(city['city'])

                    ls.logging.info("begin to send info...")
                    for user in subscribe_user:
                        try:
                            ls.logging.info("info:{},user: {}".format(push_info[:20], user))
                            itchat.send(push_info, toUserName=user)
                            # 发送太快容易出事
                            time.sleep(get_random_split())
                        except BaseException as e:
                            ls.logging.error("send failed，{}".format(user))
                            ls.logging.exception(e)
            if debug:
                break
            # 暂停几分钟
            time.sleep(get_random_long_time())
    except BaseException as e:
        ls.logging.error("Error in check ncov update-----")
        ls.logging.exception(e)

def construct_push_info(city):

    area = '{}有数据更新，新增'.format(city['city'])
    n_confirm = '确诊病例{}例'.format(city['n_confirm']) if city['n_confirm'] > 0 else ''
    n_suspect = '疑似病例{}例'.format(city['n_suspect']) if city['n_suspect'] > 0 else ''
    n_heal = '治愈病例{}例'.format(city['n_heal']) if city['n_heal'] > 0 else ''
    n_dead = '死亡病例{}例'.format(city['n_dead']) if city['n_dead'] > 0 else ''
    push_info = list(filter(lambda x: len(x) > 0, [n_confirm, n_suspect, n_heal, n_dead]))
    push_info_str = area + "、".join(push_info) + "；"

    confirm = '目前共有确诊病例{}例'.format(city['confirm'])
    suspect = '疑似病例{}例'.format(city['suspect']) if city['suspect'] > 0 else ''
    heal = '治愈病例{}例'.format(city['heal'])
    dead = '死亡病例{}例'.format(city['dead'])
    push_info = list(filter(lambda x: len(x) > 0, [confirm, suspect, heal, dead]))
    push_info_str += "、".join(push_info) + "。"
    push_info_str += get_random_tail()
    return push_info_str

def check_help(text):
    text = text.lower()
    return re.match('^help|帮助$', text) != None

