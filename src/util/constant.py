import sys
import os
import random

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
BASE_PATH = os.path.split(rootPath)[0]
sys.path.append(BASE_PATH)

#### Redis Key Begin
# 每个城市单独保存一个key做集合，订阅的用户在集合中

# 当前所有疫情数据，类型：list
STATE_NCOV_INFO = 'state_ncov_info'
# 所有有疫情的城市集合
ALL_AREA_KEY = 'all_area'
# 标记为，标记数据是有更新
SHOULD_UPDATE = 'should_update'
# 需要推送更新的数据
UPDATE_CITY = 'update_city'
# 当前已有订阅的城市集合，类型set
ORDER_KEY = 'order_area'
# 用户关注的群聊
USER_FOCUS_GROUP = 'user_focus_group'

#### Redis Key End

### Reg Pattern Begin

UN_REGIST_PATTERN = '^取关|取消(关注)?.+'
UN_REGIST_PATTERN2 = '^取关|取消(关注)?'

### REG PAttern End

BASE_DIR = BASE_PATH + '/resource/'
# for localhost redis
REDIS_HOST = '127.0.0.1'
## for docker redis
REDIS_HOST_DOCKER = 'redis'

LOGGING_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

AREA_TAIL = '(自治+)|省|市|县|区|镇'

FIRST_NCOV_INFO = '{}目前有确诊病例{}例，死亡病例{}例，治愈病例{}例'

UPDATE_NCOV_INFO = '{}有数据更新，新增确诊病例{}例，目前共有确诊病例{}例，死亡病例{}例，治愈病例{}例。为了保证您能持续收到消息，根据微信的规则，建议您偶尔回复我一下～'
UPDATE_NCOV_INFO_ALL = '{}有数据更新，新增确诊病例{}例，疑似病例{}例，目前共有确诊病例{}例，疑似病例{}例，死亡病例{}例，治愈病例{}例。为了保证您能持续收到消息，根据微信的规则，建议您偶尔回复我一下～'

NO_NCOV_INFO = '{}暂无疫情信息'

INFO_TAIL = "若{}等地区数据有更新，我会在第一时间通知您！您也可以通过发送 '取消+地区名'取消关注该地区，比如'取消{}'，'取消全国'"
INFO_TAIL_ALL = "若全国的数据有更新，我会在第一时间通知您！您也可以通过发送'取消全国'取消对全国数据的关注。"

FOCUS_TAIL = "如果该群转发的新闻截图或链接有谣言，将会自动发送辟谣链接！您也可以通过发送'取消鉴别+群名'取消对该群的谣言检查。"

TIME_SPLIT = 60 * 3

SHORT_TIME_SPLIT = 60 * 5

SEND_SPLIT = random.random() * 10

HELP_CONTENT = "您好！这是微信疫情小助手（非官方）！我有以下功能：发送 订阅/取消+地区名 关注/取消该地区疫情；发送鉴别+群名，将对该群的新闻长文、链接分享、截图自动进行辟谣，使用停止鉴别+群名停止该功能。以上所有数据来自腾讯\"疫情实时追踪\"平台，链接：https://news.qq.com//zt2020/page/feiyan.htm"
