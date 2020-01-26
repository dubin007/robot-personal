import itchat

class NcovWeRobot(object):

    def __init__(self):
        itchat.auto_login()
        itchat.send('Hello, filehelper', toUserName='filehelper')

