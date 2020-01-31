from src.robot.NcovWeRobotServer import start_server
import time
if __name__=='__main__':
    warm_tip = "****************************************\n" \
               "**************微信疫情信息小助手**************\n" \
               "****************************************"
    print(warm_tip)
    print("注意！！！稍后会弹出网页版微信登陆的二维码")
    print("登陆成功后可以开启疫情信息自动推送和群聊辟谣等功能")
    print("不会保存任何聊天记录，疫情信息和疫情订阅信息会存在您的本地")
    print("但仍然存在一定的安全风险，比如频繁使用可能会造成您最终无法登陆网页版微信")
    print("请务必谨慎使用！！！")
    time.sleep(5)
    start_server()