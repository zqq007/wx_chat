import itchat
from itchat.content import TEXT
from win11toast import toast


def send_windows(opposite, msg):
    """
    这个函数是用来弹窗
    :param opposite: 对方的名称
    :param msg: 对方发过来的信息
    :return: None
    """
    # 构建窗口
    if opposite != "":
        result = toast(opposite, msg.text, icon='D:/0.png', input='reply', button='发送')
        # print(result)
        message = result['user_input']['reply']

        # 发送信息
        if message != "":
            itchat.send_msg(message, toUserName=msg['FromUserName'])


def check_is_me():
    """
    这个函数用来提取自己的微信名，因为自己不能给自己备注，所以自己给自己的备注一定是空
    :return: 自己的备注名
    """
    my_friends = itchat.get_friends()[0:1]
    for friend in my_friends:
        return friend['NickName']


def get_head_image(opposite_img):
    """
    该函数用来保存微信头像
    :param opposite_img: 微信头像
    :return: None
    """
    # 将发信人的头像保存
    image = open('D:/0.png', 'wb')
    image.write(opposite_img)
    image.close()


def extract_info(msg):
    """
    从收到的信息中提取发信人的信息
    :param msg: 收到的信息结构体
    :return: 返回发信人的姓名
    """
    # 获取所有好友信息，并从发过来的信息中提取发信人，保存发信人的备注
    opposite = ""
    opposite_img = None
    my_friends = itchat.get_friends()
    for friend in my_friends:
        if friend['UserName'] == msg['FromUserName']:
            # 优先判断有没有备注
            if friend['RemarkName'] != "":
                opposite = friend['RemarkName']
            # 再判断这个人是不是自己，如果是自己就不管
            elif friend['NickName'] != check_is_me():
                opposite = friend['NickName']
            opposite_img = itchat.get_head_img(userName=friend['UserName'])

    # 保存发信人的头像
    get_head_image(opposite_img)

    # 把发信人的姓名返回
    return opposite


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # 提取发信人的信息
    opposite = extract_info(msg)

    # 回信息
    send_windows(opposite, msg)


itchat.auto_login(hotReload=True)
itchat.run()
