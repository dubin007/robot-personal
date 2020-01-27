import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
BASE_PATH = os.path.split(rootPath)[0]
sys.path.append(BASE_PATH)

BASE_DIR = BASE_PATH + '/resource/'

LOGGING_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
REDIS_HOST = '127.0.0.1'

STATE_NCOV_INFO = 'state_ncov_info'
ALL_AREA_KEY = 'all_area'

AREA_TAIL = '(自治+)|省|市|县|区|镇'

USER_SUBSCRIBE_KEY = 'user_subscribe'