import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
BASE_PATH = os.path.split(rootPath)[0]
sys.path.append(BASE_PATH)

#### Redis Key Begin
STATE_NCOV_INFO = 'state_ncov_info'
ALL_AREA_KEY = 'all_area'
USER_SUBSCRIBE_KEY = 'user_subscribe'
SHOULD_UPDATE = 'should_update'
UPDATE_CITY = 'update_city'
ORDER_KEY = 'order_area'
#### Redis Key End

### Reg Pattern Begin

UN_REGIST_PATTERN = '^取关|取消(关注)?.+'
UN_REGIST_PATTERN2 = '^取关|取消(关注)?'

BASE_DIR = BASE_PATH + '/resource/'
REDIS_HOST = '127.0.0.1'

LOGGING_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

AREA_TAIL = '(自治+)|省|市|县|区|镇'

FIRST_NCOV_INFO = '{}目前有确诊病例{}例，死亡病例{}例，治愈病例{}例'

UPDATE_NCOV_INFO = '{}有数据更新，新增确诊病例{}例，目前共有确诊病例{}例，死亡病例{}例，治愈病例{}例'

NO_NCOV_INFO = '{}暂无疫情信息'

INFO_TAIL = "若{}等地区数据有更新，我会在第一时间通知您！您也可以通过发送 '取消+地区名'取消关注该地区，比如'取消{}'，'取消全国'"
INFO_TAIL_ALL = "若全国的数据有更新，我会在第一时间通知您！您也可以通过发送'取消全国'取消对全国数据的关注"
TIME_SPLIT = 60 * 10

SHORT_TIME_SPLIT = 60 * 5