import json
import requests
import random
import time

url = "https://netcut.cn/api/note2"
props = {}
expire_time = 94608000      #剪切板有效时间，默认最长（3年）


def setProps(params = None):
    """
    将 note_name和 note_id写入配置文件
    :param params: 字典
    :return:
    """
    with open("props.json","w") as f:
        json.dump(params,f)
    return


def getProps():
    """
    读配置文件中的信息
    :return: 字典
    """
    try:
        with open("props.json","r") as f:
            _props = json.load(f)
    except:
        return {}
    return _props


def createNote(noteName = None):
    """
    创建剪切板
    :param noteName: 不传入默认随机生成
    :return: 成功返回True，否则返回False
    """
    if noteName is None:  #随机生成 noteName
        noteName = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890', 8)) + str(round(time.time() * 1000))
    data = {'note_name':noteName,'note_content':'null','expire_time':expire_time}
    resp = requests.post(url+'/save',data=data)
    if resp.json()['status'] != 1:
        return False
    noteId = resp.json()['data']['note_id']
    props['noteName'] = noteName
    props['noteId'] = noteId
    setProps(props)
    return True


def getinfo(noteName):
    """
    获取剪切板内容
    :param noteName: 剪切板名字
    :return: 成功返回剪切板信息，否则返回{}
    """
    data = {'note_name':noteName}
    resp = requests.post(url + '/info', data=data)
    result = resp.json()
    if result['status'] != 1:
        return {}
    return result['data']


def saveData(noteName,content):
    """
    保存信息到剪切板
    :param noteName: 剪切板名字
    :param content: 要保存的文本
    :return: 成功返回True，否则返回False
    """
    res = getinfo(noteName)
    if res == {}:
        return False
    noteId = res['note_id']
    noteToken = res['note_token']
    data = {'note_name':noteName,'note_id':noteId,'note_token':noteToken,'note_content':content,'expire_time':expire_time}
    resp = requests.post(url + '/save', data=data)
    status = resp.json()['status']
    return status == 1


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    """
    使用示例
    """
    #载入信息
    props = getProps()
    if props == {}:  #载入不成功创建新的剪切板
        createNote()

    #写数据
    flag = saveData(props['noteName'],'hello py!')
    if not flag:
        print("保存失败！检查网络或props.json文件！")

    #获取信息
    info = getinfo(props['noteName'])
    if info != {}:
        print(info['note_content'])

    input()







